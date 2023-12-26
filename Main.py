import PySimpleGUI as sg
from pytube import YouTube
from pytube.exceptions import RegexMatchError


def download(url, output_path="."):
    try:
        # Create a YouTube object using the provided URL
        yt = YouTube(url)

        # Filter and select the first stream with the "mp4" extension and marked as progressive
        video = yt.streams.filter(file_extension="mp4", progressive=True).first()

        # Download the selected video stream to the specified output path
        video.download(output_path)

        # Show a popup message indicating successful download
        sg.popup(f"Download successful. Video saved to {output_path}")

    except RegexMatchError as e:
        # Show a popup message if there is an error matching the URL pattern
        sg.popup_error(f"Error: {str(e)}. Please check your URL.")
    except Exception as e:
        # Show a popup message for other unexpected errors
        sg.popup_error(f"Error: {str(e)}")


def main():
    # Set the theme for the GUI
    sg.theme('default1')

    # Define the layout of the GUI
    layout = [
        [sg.Text("Enter video URL", font=("Calibri", 15))],
        [sg.InputText(key="URL"), sg.Button("Download")],
        [sg.Text("Select download location", font=("Calibri", 15)), sg.FolderBrowse(key="DOWNLOAD_FOLDER")],
        [sg.Text("", key="ERROR_MESSAGE", text_color="red", size=(40, 1))]
    ]

    # Create the window
    window = sg.Window("YouTube Downloader", layout)

    # Event loop
    while True:
        event, values = window.read()

        # Exit the loop if the window is closed
        if event == sg.WIN_CLOSED:
            break
        elif event == "Download":
            # Get the URL and download location from the input fields
            url = values["URL"]
            output_path = values["DOWNLOAD_FOLDER"]

            # Check if a download location is selected
            if not output_path:
                # Show an error message if no download location is selected
                window["ERROR_MESSAGE"].update("Error: Please select a download location.", text_color="red")
            else:
                # Clear any previous error messages
                window["ERROR_MESSAGE"].update("")

                # Call the download function with the provided URL and download location
                download(url, output_path)

    # Close the window when the loop exits
    window.close()


# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
