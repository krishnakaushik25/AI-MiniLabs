import os
import json
import logging
import base64
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, Dict, List
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type, wait_random_exponential
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Size limits
MAX_SIZE_OCR = 32 * 1024 * 1024  # 32 MB for OCR (fireworks_ocr)
MAX_SIZE_VISUAL = 5 * 1024 * 1024  # 5 MB for Visual API


class KYCInfo(BaseModel):
    name: str
    dob: str
    document_id: str
    expiry_date: str
    issuing_state: str
    address: Optional[str] = None  # Required only for driving licenses


@retry(
    wait=wait_random_exponential(multiplier=0.5, min=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.Timeout))
)
def download_image(url: str) -> bytes:
    """
    Downloads an image from the specified URL with retry logic.

    Args:
        url: The URL of the image to download

    Returns:
        bytes: The image content

    Raises:
        requests.exceptions.RequestException: If the download fails after all retries
    """
    try:
        logger.info("Attempting to download image from URL: %s", url)
        response = requests.get(
            url,
            timeout=30,  # 30 seconds timeout
        )
        response.raise_for_status()
        content_type = response.headers.get('content-type', '')

        # Verify we received an image
        if not content_type.startswith('image/'):
            raise ValueError(f"URL did not return an image. Got content-type: {content_type}")

        return response.content

    except requests.exceptions.Timeout:
        logger.error("Timeout while downloading image from %s", url)
        raise
    except requests.exceptions.RequestException as e:
        logger.error("Error downloading image from %s: %s", url, str(e))
        raise
    except Exception as e:
        logger.error("Unexpected error while downloading image: %s", str(e))
        raise


def encode_image_bytes(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')


def is_passport(document_id: str) -> bool:
    """
    Determines if the document_id follows the US passport format.
    For legacy US passports, we have the following 9 digits rule.
    """
    return len(document_id) == 9


def validate_kyc_fields(kyc_data: Dict) -> List[str]:
    """
    Validates the KYC data dictionary for essential fields.
    Returns a list of missing or invalid fields.

    Rules:
    - All documents require: name, dob, document_id, expiry_date, issuing_state
    - Only driving licenses require address
    - Passports (9-digit document_id) don't require address
    """
    missing_fields = []

    # Always required fields
    required_fields = ["name", "dob", "document_id", "expiry_date", "issuing_state"]
    for field in required_fields:
        value = kyc_data.get(field)
        if not value or str(value).strip().upper() == "NA":
            missing_fields.append(field)

    # Early return if document_id is missing (can't determine document type)
    if "document_id" in missing_fields:
        return missing_fields

    # Address validation only for non-passport documents
    doc_id = kyc_data.get("document_id")
    if not is_passport(doc_id):
        address = kyc_data.get("address")
        if not address or str(address).strip().upper() == "NA":
            missing_fields.append("address")

    return missing_fields


@retry(
    wait=wait_random_exponential(multiplier=0.5, min=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception)
)
def call_fireworks_ocr_kyc(document_source: str) -> Dict:
    """
    Calls the Fireworks OCR API to extract KYC details
    using document inlining.
    """
    try:
        logger.info("Calling OCR API with document source.")
        response = client.chat.completions.create(
            model="accounts/fireworks/models/qwen2p5-72b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": document_source}
                        },
                        {
                            "type": "text",
                            "text": (
                                "Extract the following KYC fields from the document in JSON format: "
                                "name, dob, document_id, expiry_date, address, and issuing_state. "
                                "Rules:\n"
                                "1. Name must include valid first and last name (never NA).\n"
                                "2. The document is either a US State driving license or a US passport.\n"
                                "3. For driving licenses, the document will contain a US state name and an address.\n"
                                "4. For US passports, the document_id is nine digits and "
                                "address should be returned as NA; issuing_state must be provided.\n"
                                "5. For driving licenses, document_id may be in various formats (e.g., 'DL 12345', 'DN 12345', 'DLN 12345') "
                                "where only the numeric part is needed.\n"
                                "6. Date format is MM/DD/YYYY."
                            )
                        }
                    ]
                }
            ],
            response_format={
                "type": "json_object",
                "schema": KYCInfo.model_json_schema()
            }
        )
        json_string = response.choices[0].message.content
        result = json.loads(json_string)
        logger.info("OCR API extraction result: %s", result)
        return result
    except Exception as e:
        logger.error("Error during OCR API call: %s", e)
        raise


@retry(
    wait=wait_random_exponential(multiplier=0.5, min=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception)
)
def call_fireworks_visual_api_missing_fields(missing_fields: List[str], base64_image: str) -> Dict:
    """
    Calls the Fireworks Visual API to extract all missing fields in one call.
    This text is then passed to the reasoning
    model to extract the missing fields in JSON format.
    """
    prompt_text = f"Extract the following fields from the document: {', '.join(missing_fields)}"
    try:
        logger.info("Calling Visual API for missing fields: %s", missing_fields)
        response = client.chat.completions.create(
            model="accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                    {
                        "type": "text",
                        "text": prompt_text
                    }
                ]
            }]
        )
        visual_text = response.choices[0].message.content.strip()
        logger.info("Visual API returned text: %s", visual_text)
        # Use the reasoning model to extract missing fields from the visual text.
        result = call_reasoning_model_for_missing_fields(missing_fields, visual_text)
        return result
    except Exception as e:
        logger.error("Error during Visual API call: %s", e)
        raise


@retry(
    wait=wait_random_exponential(multiplier=0.5, min=1, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type(Exception)
)
def call_reasoning_model_for_missing_fields(missing_fields: List[str], visual_text: str) -> Dict:
    """
    Uses the reasoning model to extract the missing fields from the provided visual API text.
    Implements jitter in retry logic to prevent synchronized retries.
    """
    prompt_text = (
        "Based on the following extracted text from the document:\n"
        f"{visual_text}\n\n"
        f"Extract the following missing fields in JSON format: {', '.join(missing_fields)}.\n"
        "Rules:\n"
        "1. For 'name', ensure it includes both first and last name.\n"
        "2. For 'address', provide the full address if available.\n"
        "3. Use the date format MM/DD/YYYY for any dates.\n"
        "4. If the value of the missing fields is Not available, then assign 'NA' to it."
    )
    try:
        response = client.chat.completions.create(
            model="accounts/fireworks/models/qwen2p5-72b-instruct",
            messages=[{
                "role": "user",
                "content": [{"type": "text", "text": prompt_text}]
            }],
            response_format={"type": "json_object"}
        )
        json_string = response.choices[0].message.content
        result = json.loads(json_string)
        logger.info("Reasoning model extracted missing fields: %s", result)
        return result
    except Exception as e:
        logger.error("Error during reasoning model call: %s", e)
        raise


def main():
    """
    Main function to download the image, extract KYC details via OCR,
    and if necessary, extract missing fields using the Visual API and reasoning model.
    If the Visual API extraction does not populate the missing fields,
    reattempt up to 3 times before failing.
    """
    image_url = "https://drive.google.com/uc?export=download&id=1OwDlWQ4z0SrNKo1TYRDsYxnc-Ai_-jtl"

    try:
        # Download and encode image
        image_bytes = download_image(image_url)
        image_size = len(image_bytes)
        logger.info("Downloaded image size: %.2f MB", image_size / (1024 * 1024))

        if image_size > MAX_SIZE_OCR:
            raise ValueError("Image size exceeds the 32 MB limit for OCR processing.")

        image_base64 = encode_image_bytes(image_bytes)

        # Prepare document source for OCR (with document inlining)
        document_source = f"data:image/jpeg;base64,{image_base64}#transform=inline"
        ocr_result = call_fireworks_ocr_kyc(document_source)

        # Validate and determine missing fields (taking document type into account)
        missing_fields = validate_kyc_fields(ocr_result)
        logger.info("Fields missing after OCR extraction: %s", missing_fields)

        # If missing fields exist, attempt up to 3 times to extract them using the Visual API.
        if missing_fields:
            if image_size > MAX_SIZE_VISUAL:
                logger.error("Image size (%.2f MB) exceeds the 5 MB limit for Visual API extraction.",
                             image_size / (1024 * 1024))
                raise ValueError("Cannot use Visual API as image size exceeds 5 MB limit.")

            max_visual_attempts = 3
            attempts = 0
            while missing_fields and attempts < max_visual_attempts:
                attempts += 1
                logger.info("Visual extraction attempt %d for missing fields: %s", attempts, missing_fields)
                visual_result = call_fireworks_visual_api_missing_fields(missing_fields, image_base64)
                # Update OCR result with the new values if valid.
                ocr_result.update({k: v for k, v in visual_result.items() if v and str(v).strip().upper() != "NA"})
                missing_fields = validate_kyc_fields(ocr_result)
                logger.info("Missing fields after visual extraction attempt %d: %s", attempts, missing_fields)

            if missing_fields:
                error_msg = f"Final KYC extraction missing fields after {attempts} attempts: {missing_fields}"
                logger.error(error_msg)
                raise ValueError(error_msg)

        # Build final KYCInfo model and output the result.
        final_kyc = KYCInfo(**ocr_result)
        final_json = final_kyc.model_dump_json()
        logger.info("Final KYC Information: %s", final_json)
        print(final_json)

    except Exception as e:
        logger.error("Error in main processing: %s", e)


if __name__ == "__main__":
    client = openai.OpenAI(
        base_url="https://api.fireworks.ai/inference/v1",
        api_key=os.getenv("FIREWORKS_API_KEY")
    )
    main()