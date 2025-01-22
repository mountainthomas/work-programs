import pandas as pd


def analyze_csv(file_path):
    # Read CSV and skip first 8 rows
    df = pd.read_csv(file_path, skiprows=8)

    # Ensure columns exist
    if len(df.columns) < 7:
        return "CSV must have at least 7 columns"

    # Get names from column 2 (index 1) and values from column 7 (index 6)
    names = df.iloc[:, 1]
    values = df.iloc[:, 6]

    # Create dictionary to store totals
    totals = {}
    current_name = None
    current_total = 0

    # Calculate totals
    for name, value in zip(names, values):
        # If name is NaN/empty, use previous name
        if pd.isna(name) or str(name).strip() == '':
            name = current_name
        else:
            current_name = name

        try:
            value = float(value)
            totals[name] = totals.get(name, 0) + value
        except (ValueError, TypeError):
            continue

    # Convert to DataFrame and sort
    result_df = pd.DataFrame(list(totals.items()), columns=['Name', 'Total'])
    result_df = result_df.nlargest(15, 'Total')

    return result_df


if __name__ == "__main__":
    file_path = input("Enter CSV file path: ")
    try:
        result = analyze_csv(file_path)
        print("\nTop 15 totals:")
        print(result)
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(f"Error: {e}")