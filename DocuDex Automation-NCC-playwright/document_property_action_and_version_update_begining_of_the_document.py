from common import (
    new_page,
    login,
    DOCUMENT_USER,
    DOCUMENT_PASSWORD,
    PDF_DIR,
    OCR_DIR,
    upload_and_search_test_document,
    download_and_send_for_review,
    edit_properties_and_extend_expiry,
    upload_new_version,
    upload_second_version_for_merge,
    choose_merge_position,
    choose_minor_changes_and_save,
)

with new_page() as page:
    login(page, DOCUMENT_USER, DOCUMENT_PASSWORD)

    upload_and_search_test_document(page)

    download_and_send_for_review(page)

    edit_properties_and_extend_expiry(page, "This Document Edited")

    upload_new_version(page, OCR_DIR / "ocr.pdf", "Uploaded new Version of this document")

    upload_second_version_for_merge(page, PDF_DIR / "file-example_PDF_1MB.pdf")

    choose_merge_position(page, "Beginning of the document")

    choose_minor_changes_and_save(
        page,
        "Document has been mergered at the beginning of the document as Minor changes Version",
    )

    page.reload()

    input("Check UI. Press Enter to close browser...")
