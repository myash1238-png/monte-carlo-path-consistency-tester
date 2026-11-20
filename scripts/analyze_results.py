from monte_carlo.database.db import connect
from monte_carlo.database.repository import variance_across_seeds, list_results

def main():
    with connect() as conn:
        for row in list_results(conn):
            print(dict(row))
        row = variance_across_seeds(conn)
        print("\\nVariance across GBM seeds:")
        print(dict(row) if row else "No GBM records found")

if __name__ == "__main__":
    main()
