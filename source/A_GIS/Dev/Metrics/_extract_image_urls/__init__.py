def _extract_image_urls(issue, url):
    """Extract image URLs from issue description and notes.

    Args:
        issue (gitlab.v4.objects.Issue): GitLab issue object.
        url (str): Base GitLab URL.

    Returns:
        list: List of dicts containing image info.
    """
    import re
    import os

    images = []

    # Function to extract upload URLs
    def find_uploads(text):
        if not text:
            return []
        matches = re.findall(
            r'/uploads/[a-f0-9]+/[^\s"\']+\.(?:png|jpg|gif|jpeg|webp)', text
        )
        return [
            {"link": m, "url": f"{url}{m}"} for m in matches
        ]

    # Get images from description
    images.extend(find_uploads(issue.description))

    # Get images from notes
    for note in issue.notes.list(all=True):
        images.extend(find_uploads(note.body))

    return images
