"""
Databricks Connection Helper
Supports multiple authentication methods to connect to your default workspace
"""

import os
from databricks import sql
from databricks.sdk import WorkspaceClient


class DatabricksConnector:
    """Helper class to connect to Databricks using various authentication methods"""
    
    def __init__(self):
        self.connection = None
        self.client = None
    
    # Method 1: Connect using default profile from ~/.databrickscfg
    def connect_with_default_profile(self):
        """
        Connects using the DEFAULT profile from ~/.databrickscfg
        
        Your ~/.databrickscfg should look like:
        [DEFAULT]
        host = https://your-workspace.cloud.databricks.com
        token = dapi...
        """
        try:
            # Databricks SDK will automatically use DEFAULT profile
            self.client = WorkspaceClient()
            print("✓ Connected to Databricks using default profile")
            print(f"  Workspace: {self.client.config.host}")
            return self.client
        except Exception as e:
            print(f"✗ Failed to connect with default profile: {e}")
            return None
    
    # Method 2: Connect to SQL Warehouse using default profile
    def connect_sql_warehouse(self, http_path=None):
        """
        Connects to SQL Warehouse using default profile
        
        Args:
            http_path: SQL Warehouse HTTP path (e.g., /sql/1.0/warehouses/abc123)
                      If None, you'll need to set it in ~/.databrickscfg
        """
        try:
            # Get credentials from default profile
            from databricks.sdk.core import Config
            config = Config()
            
            host = config.host
            token = config.token
            
            if not http_path:
                http_path = os.getenv('DATABRICKS_HTTP_PATH')
            
            if not http_path:
                print("✗ HTTP path not provided. Please specify SQL Warehouse path.")
                return None
            
            self.connection = sql.connect(
                server_hostname=host.replace('https://', ''),
                http_path=http_path,
                access_token=token
            )
            
            print("✓ Connected to Databricks SQL Warehouse")
            print(f"  Host: {host}")
            print(f"  HTTP Path: {http_path}")
            return self.connection
            
        except Exception as e:
            print(f"✗ Failed to connect to SQL Warehouse: {e}")
            return None
    
    # Method 3: Connect using environment variables
    def connect_with_env_vars(self):
        """
        Connects using environment variables:
        - DATABRICKS_HOST
        - DATABRICKS_TOKEN
        """
        try:
            host = os.getenv('DATABRICKS_HOST')
            token = os.getenv('DATABRICKS_TOKEN')
            
            if not host or not token:
                print("✗ DATABRICKS_HOST and DATABRICKS_TOKEN must be set")
                return None
            
            self.client = WorkspaceClient(host=host, token=token)
            print("✓ Connected to Databricks using environment variables")
            print(f"  Workspace: {host}")
            return self.client
            
        except Exception as e:
            print(f"✗ Failed to connect with environment variables: {e}")
            return None
    
    def execute_query(self, query):
        """Execute a SQL query on the connected warehouse"""
        if not self.connection:
            print("✗ No SQL connection established. Call connect_sql_warehouse() first.")
            return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"✗ Query failed: {e}")
            return None
    
    def close(self):
        """Close the connection"""
        if self.connection:
            self.connection.close()
            print("✓ Connection closed")


# Example Usage
if __name__ == "__main__":
    print("=" * 60)
    print("Databricks Connection Test")
    print("=" * 60)
    
    connector = DatabricksConnector()
    
    # Try Method 1: Connect using default profile
    print("\n[Method 1] Connecting with default profile...")
    client = connector.connect_with_default_profile()
    
    if client:
        # Test the connection by listing catalogs
        try:
            catalogs = list(client.catalogs.list())
            print(f"\n✓ Available catalogs ({len(catalogs)}):")
            for catalog in catalogs[:5]:  # Show first 5
                print(f"  - {catalog.name}")
        except Exception as e:
            print(f"✗ Could not list catalogs: {e}")
    
    # Uncomment to test SQL Warehouse connection:
    # print("\n[Method 2] Connecting to SQL Warehouse...")
    # http_path = "/sql/1.0/warehouses/YOUR_WAREHOUSE_ID"
    # connection = connector.connect_sql_warehouse(http_path)
    # 
    # if connection:
    #     results = connector.execute_query("SELECT current_user()")
    #     print(f"Current user: {results}")
    
    # Clean up
    connector.close()
    
    print("\n" + "=" * 60)
    print("Setup Instructions:")
    print("=" * 60)
    print("""
    To use the default profile, create ~/.databrickscfg:
    
    [DEFAULT]
    host = https://your-workspace.cloud.databricks.com
    token = dapi...
    
    To get your token:
    1. Log into your Databricks workspace
    2. Click your username (top right) → Settings
    3. Go to Developer → Access tokens
    4. Click 'Generate new token'
    5. Copy the token to ~/.databrickscfg
    """)


