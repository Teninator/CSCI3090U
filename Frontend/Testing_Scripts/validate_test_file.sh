#!/bin/bash

# Root directory where test cases are stored
TEST_ROOT="../../Tests"

# Default verbose mode
VERBOSE=true

# Parse command-line arguments
for arg in "$@"; do
    case $arg in
        --verbose=false)
            VERBOSE=false
            shift
            ;;
    esac
done

echo "🔍 Starting validation of test file comparisons at $(date)"

# Prompt user to choose between comparing all transactions or a specific one
echo "Select an option:"
echo "1. Compare all transactions"
echo "2. Compare a specific transaction"
read -p "Enter your choice (1 or 2): " choice

# Function to compare test files for a specific transaction
compare_transaction() {
    TRANSACTION_NAME="$1"
    TRANSACTION_DIR="$TEST_ROOT/$TRANSACTION_NAME/"
    echo "Entering transaction type: $TRANSACTION_NAME"

    # Loop through each test directory for the current transaction
    for TEST_DIR in "$TRANSACTION_DIR"*/; do
        TEST_NAME=$(basename "$TEST_DIR")
        echo "Comparing test case: $TRANSACTION_NAME - $TEST_NAME"

        # Define file paths based on test structure
        EXPECTED_TRANSACTION_FILE="$TEST_DIR/${TEST_NAME}.etf.txt"
        ACTUAL_TRANSACTION_FILE="$TEST_DIR/${TEST_NAME}.atf.txt"
        EXPECTED_OUTPUT_FILE="$TEST_DIR/${TEST_NAME}.bto.txt"
        ACTUAL_OUTPUT_FILE="$TEST_DIR/${TEST_NAME}.out.txt"

        if [[ "$VERBOSE" == true ]]; then
            echo "Checking required files..."
            echo "  Expected Transaction File: $(basename "$EXPECTED_TRANSACTION_FILE")"
            echo "  Actual Transaction File: $(basename "$ACTUAL_TRANSACTION_FILE")"
            echo "  Expected Output File: $(basename "$EXPECTED_OUTPUT_FILE")"
            echo "  Actual Output File: $(basename "$ACTUAL_OUTPUT_FILE")"
        fi

        # Check if all necessary files exist
        if [[ -f "$EXPECTED_TRANSACTION_FILE" && -f "$ACTUAL_TRANSACTION_FILE" && -f "$EXPECTED_OUTPUT_FILE" && -f "$ACTUAL_OUTPUT_FILE" ]]; then
            if [[ "$VERBOSE" == true ]]; then
                echo "✅ All required files found. Starting comparison..."
            fi

            # Compare transaction files
            DIFF_OUTPUT=$(diff "$EXPECTED_TRANSACTION_FILE" "$ACTUAL_TRANSACTION_FILE")
            if [[ -z "$DIFF_OUTPUT" ]]; then
                echo "✅ $(basename "$EXPECTED_TRANSACTION_FILE") matches $(basename "$ACTUAL_TRANSACTION_FILE")"
            else
                echo "❌ $(basename "$EXPECTED_TRANSACTION_FILE") differs from $(basename "$ACTUAL_TRANSACTION_FILE")"
                if [[ "$VERBOSE" == true ]]; then
                    echo "$DIFF_OUTPUT"
                fi
            fi

            # Compare output files
            DIFF_OUTPUT=$(diff "$EXPECTED_OUTPUT_FILE" "$ACTUAL_OUTPUT_FILE")
            if [[ -z "$DIFF_OUTPUT" ]]; then
                echo "✅ $(basename "$EXPECTED_OUTPUT_FILE") matches $(basename "$ACTUAL_OUTPUT_FILE")"
            else
                echo "❌ $(basename "$EXPECTED_OUTPUT_FILE") differs from $(basename "$ACTUAL_OUTPUT_FILE")"
                if [[ "$VERBOSE" == true ]]; then
                    echo "$DIFF_OUTPUT"
                fi
            fi
        else
            echo "❌ Missing required files for test: $TEST_NAME"
        fi

        # Prompt for approval to continue to the next test
        if [[ "$VERBOSE" == true ]]; then
            echo "-------------------------------------------"
            read -p "Press [Enter] to compare the next test or [Ctrl+C] to stop."
        fi
    done
}

# Handle user choice
if [[ "$choice" -eq 1 ]]; then
    # Compare all transactions
    for TRANSACTION_DIR in "$TEST_ROOT"/*/; do
        TRANSACTION_NAME=$(basename "$TRANSACTION_DIR")
        compare_transaction "$TRANSACTION_NAME"
    done
elif [[ "$choice" -eq 2 ]]; then
    # Compare a specific transaction
    echo "Available transactions:"
    # List all available transaction names
    for TRANSACTION_DIR in "$TEST_ROOT"/*/; do
        TRANSACTION_NAME=$(basename "$TRANSACTION_DIR")
        echo "- $TRANSACTION_NAME"
    done

    # Get the transaction name to compare
    read -p "Enter the transaction name to compare: " transaction_name
    if [[ -d "$TEST_ROOT/$transaction_name" ]]; then
        compare_transaction "$transaction_name"
    else
        echo "❌ Transaction '$transaction_name' not found!"
    fi
else
    echo "❌ Invalid choice! Please select 1 or 2."
fi

echo "🎯 All comparisons completed at $(date)!"
