import PyPDF2


def replace_text_in_pdf(input_path, output_path, old_text, new_text):
    # Open the input PDF file
    with open(input_path, 'rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)

        # Create a PDF writer object
        writer = PyPDF2.PdfWriter()

        # Iterate through each page in the PDF
        for page in reader.pages:

            # Replace the old text with the new text in the page content
            page_text = page.extract_text()
            new_page_text = page_text.replace(old_text, new_text)
            page.merge_page(page)
            page.merge_page(new_page_text)

            # Add the modified page to the PDF writer
            writer.add_page(page)

        # Write the modified PDF to the output file
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)


if __name__ == "__main__":
    # Provide the input and output file paths
    input_pdf_path = 'atestado.pdf'  # Replace with your input PDF file
    # Replace with the desired output PDF file
    output_pdf_path = 'atestado_output.pdf'

    # Specify the old and new text to be replaced
    # Replace with the old text you want to replace
    old_text_to_replace = 'Luiza Hooper Moretti'
    # Replace with the new text you want to insert
    new_text_to_insert = 'Nicolas Chagas Souza'

    # Call the function to replace text in the PDF
    replace_text_in_pdf(input_pdf_path, output_pdf_path,
                        old_text_to_replace, new_text_to_insert)

    print(
        f"Text replaced successfully. Modified PDF saved to '{output_pdf_path}'.")
