from scanner.form_finder import find_forms

if __name__ == "__main__":
    url = input("Enter target URL: ").strip()
    find_forms(url)
