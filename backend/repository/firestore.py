from firebase_admin import firestore

_db = firestore.client()

def save(collection: str, document: str, data: dict):
    doc_ref = _db.collection(collection).document(document)
    doc_ref.set(data)

def get(collection: str, document: str):
    doc_ref = _db.collection(collection).document(document)
    doc = doc_ref.get()
    if doc._exists:
        return {
            'id': doc.id,
            **doc.to_dict()
        }
    else:
        return None

def get_all(collection: str):
    doc_ref = _db.collection(collection)
    docs = doc_ref.get()
    results = []
    for doc in docs:
        results.append({
            'id': doc.id,
            **doc.to_dict()
        })
    return results

def delete(collection: str, document: str):
    doc_ref = _db.collection(collection).document(document)
    doc_ref.delete()

def delete_all(collection: str, mark_for_delete):
    doc_ref = _db.collection(collection)
    docs = doc_ref.get()
    for doc in docs:
        if (mark_for_delete(doc.to_dict())):
            doc.reference.delete()