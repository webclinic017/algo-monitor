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

# def teste():
#     doc_ref = _db.collection(u'users').document(u'alovelace')
#     doc_ref.set({
#         u'first': u'Ada',
#         u'last': u'Lovelace',
#         u'born': 1815
#     })
    
#     doc_ref = _db.collection(u'users').document(u'aturing')
#     doc_ref.set({
#         u'first': u'Alan',
#         u'middle': u'Mathison',
#         u'last': u'Turing',
#         u'born': 1912
#     })
#     users_ref = _db.collection(u'users')
#     docs = users_ref.get()
#     for doc in docs:
#         print(u'{} => {}'.format(doc.id, doc.to_dict()))