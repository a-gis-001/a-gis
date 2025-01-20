def get_nearest(
    *,
    target_path: str,
    collection_name: str,
    database_name: str,
    num: int = 5,
    min_similarity: float = 0.7,
    ignore_list=["_inbox"],
    keep_list=[],
):
    """Find nearest document in a database collection by embedding.

    This function searches for the `num` closest documents to a target
    document within a specified collection and database, based on their
    vector embeddings. The closeness is determined by calculating the
    angle between the embedding vectors of the target and each document.
    The function filters out documents in the `ignore_list` and only
    includes those in the `keep_list`.

    The nearest documents are sorted by their distance to the target,
    and the top `num` results are returned as a structured object. This
    allows for easy access to both the nearest documents' information
    and the parameters used for the search.

    Args:
        target_path (str):
            The path of the target document within the collection.
        collection_name (str):
            The name of the collection from which to find the nearest
            documents.
        database_name (str):
            The name of the database containing the collection.
        num (int, optional):
            The number of nearest documents to return. Defaults to 5.
        min_similarity (float, optional):
            The minimum similarity to collect, between 0 and 1. Default to 0.7.
        ignore_list (list, optional):
            A list of paths or patterns to ignore when searching for
            nearest documents. Defaults to ['_inbox'].
        keep_list (list, optional):
            A list of paths or patterns to only consider when searching
            for nearest documents. It overrides the `ignore_list`.

    Returns:
        make_struct:
            A structured object with the following attributes:

            - nearest (list of tuples): A sorted list of tuples
              containing the calculated angle and path of the nearest
              documents.
            - target_path (str): The path of the target document.
            - target_exists (bool): Whether the target document exists
              at its specified path.
            - collection_name (str): The name of the collection from
              which the nearest documents were found.
            - database_name (str): The name of the database containing
              the collection.
            - num (int): The number of nearest documents to return.
            - ignore_list (list of str): The list of paths or patterns
              used to filter out documents.
            - keep_list (list of str): The list of paths or patterns
              that were used to only consider certain documents.
    """
    import math
    import A_GIS.Math.calculate_angle_between_vectors
    import A_GIS.Code.make_struct
    import os
    import A_GIS.File.Management.get_collection

    target_exists = os.path.exists(target_path)
    target_path = str(target_path)
    if target_exists:
        collection = A_GIS.File.Management.get_collection(
            name=collection_name, from_database=database_name
        )
        target = collection.find_one({"_id": target_path})
        nearest = []
        if target:
            et = target.get("embedding")

            alldoc = list(collection.find())

            for doc in alldoc:
                doc_path = doc["_id"]

                # Only get for existing path.
                if not os.path.exists(doc_path):
                    continue

                # Do not check same path.
                if target_path == doc_path:
                    continue

                # Potentially skip.
                skip = False
                for i in ignore_list:
                    if i in doc_path:
                        skip = True

                for k in keep_list:
                    if not k in doc_path:
                        skip = True
                if skip:
                    continue

                # Calculate angle.
                e1 = doc.get("embedding")
                if e1 and et:
                    similarity = math.cos(
                        math.fabs(
                            A_GIS.Math.calculate_angle_between_vectors(
                                a=e1, b=et
                            ).signed_angle
                        )
                    )
                    if similarity > min_similarity:
                        nearest.append([similarity, doc_path])

        # Get num nearest.
        nearest = sorted(nearest, key=lambda x: abs(x[0]), reverse=True)[:num]

        return A_GIS.Code.make_struct(
            nearest=nearest,
            target_path=target_path,
            target_exists=target_exists,
            collection_name=collection_name,
            database_name=database_name,
            num=num,
            ignore_list=ignore_list,
            keep_list=keep_list,
        )
