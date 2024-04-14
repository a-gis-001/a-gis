def encode(*, encoder, images, batch_size=64, show_progress_bar=True):
    return encoder.encode(
        images,
        batch_size=batch_size,
        convert_to_tensor=True,
        show_progress_bar=show_progress_bar,
    )
