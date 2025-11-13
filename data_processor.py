import time

class DataHandlerAndProcessor: # CODE SMELL: Large Class
    """
    Handles data retrieval, cleaning, transformation, and report generation.
    Does too many things, violating the Single Responsibility Principle.
    """

    def __init__(self, source_url, max_records=5000):
        # CODE SMELL: Magic Number in default argument
        self.data_source = source_url
        self.data_cache = {}
        self.MAX_RECORDS = max_records
        self.status = "uninitialized"

    def fetch_data_and_process_reports(self, query_id, level, is_admin_request): # CODE SMELL: Long Method, Long Parameter List
        """
        Fetches raw data, cleans it, processes it, and generates a final report.
        This function handles too many different responsibilities.
        """
        self.status = "fetching"
        print(f"[{time.ctime()}] Starting process for query_id: {query_id}")

        # Simulate data fetching
        if query_id in self.data_cache:
            raw_data = self.data_cache[query_id]
        else:
            # CODE SMELL: Magic String/Hardcoded Value for data path
            raw_data = self._simulate_fetch_from_db(f"{self.data_source}/data/{query_id}")
            self.data_cache[query_id] = raw_data

        if not raw_data:
            return "ERROR: No data found."

        # Data Cleaning Logic
        self.status = "cleaning"
        clean_data = []
        for row in raw_data:
            # CODE SMELL: Deep Nesting (Indentation Hell)
            if row and len(row) > 2:
                # CODE SMELL: Primitive Obsession (using list indexes instead of a named structure)
                if row[1] != 'INVALID':
                    if level == 'L1' and row[2] > 100: # CODE SMELL: Magic Number (100)
                        clean_data.append(row)
                    elif level == 'L2' and row[2] > 50: # CODE SMELL: Magic Number (50)
                        clean_data.append(row)

        # Data Processing/Aggregation Logic
        self.status = "processing"
        total_value = 0
        result_map = {}

        for item in clean_data:
            # CODE SMELL: Duplicate Code (same check logic as in cleaning)
            if item[1] != 'INVALID': 
                total_value += item[2]
                key = item[0].upper()
                if key not in result_map:
                    result_map[key] = {'count': 0, 'sum': 0}
                result_map[key]['count'] += 1
                result_map[key]['sum'] += item[2]

        # Final Report Generation Logic
        self.status = "reporting"
        
        # CODE SMELL: Unused Parameter (is_admin_request isn't used)
        
        report = {
            "query_id": query_id,
            "total_processed_items": len(clean_data),
            "grand_total": total_value,
            "summary_by_key": result_map,
            "timestamp": time.time()
        }

        print(f"Process complete. Grand Total: {total_value}")
        self.status = "complete"
        return report

    def _simulate_fetch_from_db(self, path):
        """Simulates a database call and returns a list of lists (raw data)."""
        # [key_name, status, value]
        if 'users' in path:
            return [['A1', 'VALID', 150], ['B2', 'VALID', 40], ['C3', 'VALID', 110], ['D4', 'INVALID', 70]]
        return []

    def log_status(self):
        """Simple status logger."""
        print(f"Current handler status: {self.status}")


if __name__ == '__main__':
    # Example usage that demonstrates the function's complexity
    processor = DataHandlerAndProcessor("http://api.internal.com/data_v1")
    report_L1 = processor.fetch_data_and_process_reports("users_weekly", 'L1', False)
    print("\n--- L1 Report ---")
    print(report_L1)
    
    report_L2 = processor.fetch_data_and_process_reports("users_monthly", 'L2', True)
    print("\n--- L2 Report ---")
    print(report_L2)

    