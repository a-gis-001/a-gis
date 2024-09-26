def get_nearest(
    *,
    target_path: str,
    collection_name: str,
    database_name: str,
    num: int = 5,
    ignore_list=[],
    keep_list=[],
):
    """Find nearest documents by vector similarity in MongoDB.

    This function retrieves a collection from a specified database
    within A_GIS and calculates the similarity of each document's
    embedding to the target's embedding using the Haversine formula
    (implemented by `A_GIS.Math.calculate_angle_between_vectors`). It
    returns a struct containing the `num` nearest documents, sorted by
    their distance from the target's embedding, along with information
    about the target path and whether it exists.

    Args:
        target_path (str):
            The target document's path for which to find the nearest
            neighbors.
        collection_name (str):
            The name of the MongoDB collection to search within.
        database_name (str):
            The name of the MongoDB database from which to retrieve the
            collection.
        num (int, optional):
            The number of nearest neighbor documents to return. Defaults
            to 5.
        ignore_list (list, optional):
            A list of strings to filter out documents whose paths
            contain these strings.
        keep_list (list, optional):
            A list of strings that, if not present in a document's path,
            will include that document in the search results.

    Returns:
        dataclass:
            With the following attributes

            - nearest (list of tuples): A list of tuples containing
              two elements. The first is the absolute value of the
              signed angle between the target and the document's
              embeddings, and the second is the path of the document.
              These are sorted by the angle in ascending order.
            - target_path (str): The path of the target document.
            - target_exists (bool): A boolean indicating whether the
              target document exists at its specified path.
    """
    import math
    import A_GIS.Math.calculate_angle_between_vectors
    import A_GIS.Code.make_struct
    import os
    import A_GIS.File.Database.get_collection

    target_exists = os.path.exists(target_path)
    target_path = str(target_path)
    if target_exists:
        collection = A_GIS.File.Database.get_collection(
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
                    angle = A_GIS.Math.calculate_angle_between_vectors(
                        a=e1, b=et
                    ).signed_angle
                    nearest.append([math.fabs(angle), doc_path])

        # Get num nearest.
        nearest = sorted(nearest, key=lambda x: abs(x[0]))[:num]

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
