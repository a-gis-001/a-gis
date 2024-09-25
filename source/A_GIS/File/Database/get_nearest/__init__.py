def get_nearest(
    *, target_path, collection, num: int = 5, ignore_list=[], keep_list=[]
):
    """Retrieve `num` closest items by vector similarity.

    This function finds the nearest items in a MongoDB collection to a
    given target item's embedding vector. It considers a set of
    criteria, including an optional ignore list and a keep list, to
    filter out documents before calculating their similarity to the
    target. The function returns a structured result containing the
    `num` closest items sorted by their distance from the target's
    embedding vector.

    Args:
        target_path (str):
            The path identifier of the target item within the
            collection.
        collection (MongoDB collection object):
            The collection from which to retrieve the nearest items.
        num (int, optional):
            The number of closest items to return. Defaults to 5.
        ignore_list (list of str, optional):
            A list of strings (patterns) that, if matched with a
            document's path, will cause the document to be ignored.
        keep_list (list of str, optional):
            A list of strings (patterns) that must be matched with a
            document's path for the document to be considered.

    Returns:
        dataclass:
            With the following attributes

            - nearest (list of tuples): A sorted list of tuples
              containing two elements; the first is the absolute value
              of the signed angle between the target and each item's
              embedding vector, and the second is the document's path.
            - target_path (str): The path identifier of the target
              item.
            - target_exists (bool): A boolean indicating whether the
              target item exists at the specified path.
    """
    import math
    import A_GIS.Math.calculate_angle_between_vectors
    import A_GIS.Code.make_struct
    import os

    target_exists = os.path.exists(target_path)
    target_path = str(target_path)
    if target_exists:
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
        )
