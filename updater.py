import sys
import requests
import shutil
import zipfile
import os
import to_update
def update(verbose=True):
    link = 'https://github.com/KevinAS28/Management-Beras/archive/refs/heads/main.zip'
    file_name = 'main.zip'
    with open(file_name, 'wb+') as f:
        if verbose:
            print('Downloading %s' % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.flush()

    cwd = os.getcwd()
    zip_file_name = "main.zip"
    zip_main_dir = 'Management-Beras-main'

    with zipfile.ZipFile(zip_file_name) as zip_file:
        for member in to_update.to_update:
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue
        
            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            target_path = os.path.join(cwd, os.path.join(*(member.split('/')[1:])))
            if verbose:
                print(f'Updating {target_path}')
            target = open(target_path, "wb")
            with source, target:
                shutil.copyfileobj(source, target)

    os.remove(os.path.join(os.getcwd(), zip_file_name))


    for to_remove in to_update.to_remove:
        try:
            os.remove(to_remove)
        except:
            print('Gagal hapus ', to_remove)
    if verbose:
        print('Update selesai')

if __name__=='__main__':
    update()