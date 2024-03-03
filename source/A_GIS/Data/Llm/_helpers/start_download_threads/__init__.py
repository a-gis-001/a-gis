def start_download_threads(
    session, file_list, output_folder, start_from_scratch=False, threads=4
):
    import A_GIS.File.download
    from tqdm.contrib.concurrent import thread_map

    thread_map(
        lambda url: A_GIS.File.download(
            session, url, output_folder, start_from_scratch=start_from_scratch
        ),
        file_list,
        max_workers=threads,
        disable=True,
    )
