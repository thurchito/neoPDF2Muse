#!/bin/bash

# Run the setup script
./setup.sh

while true; do
    # Run the main script
    ./run_pdf2muse.sh

    # Prompt the user via CLI
    echo ""
    echo "Would you like to process another file?"
    echo "1) Yes, start new conversion"
    echo "2) No, quit and clean up"
    read -p "Enter your choice (1 or 2): " choice

    case "$choice" in
        1)
            # Loop back to start new conversion
            continue
            ;;
        2)
            # Exit the script
            echo "Exiting. Cleaning up..."
            break
            ;;
        *)
            # Invalid input, exit
            echo "Invalid choice. Exiting."
            break
            ;;
    esac
done
