from app.integrations.qdrant.client import get_qdrant_connection

def main():
  connection = get_qdrant_connection()
  client = connection.get_client()
  collection_name = connection.collection_name
  
  exists = client.collection_exists(
    collection_name=collection_name
  )
  
  print(f"Collection name: {collection_name}")
  print(f"Collection exists: {exists}")
  
  if exists:
    collection_info = client.get_collection(
      collection_name=collection_name
    )
    
    print(f"Collectionm status: {collection_info.status}")
    print(
      "Vector configuration:",
      collection_info.config.params.vectors
    )
    print(
      "Points count:",
      collection_info.points_count,
    )
  else:
    print(
      "Collection belum tersedia. "
      "Collection perlu dibuat sebelum FAQ dapat diindeks."
    )
    
if __name__ == "__main__":
  main()