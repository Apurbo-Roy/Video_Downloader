import selfPlaylist
import threading
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube, request

file_size = 0


# dark mode :
def dark_mode():
    global btnState
    if btnState:
        btn.config(image=offImg, bg="#f0f0f0", activebackground="#f0f0f0")
        root.config(bg="#f0f0f0")
        txt.config(text="Dark Mode: OFF", bg="#f0f0f0")
        btnState = False
    else:
        btn.config(image=onImg, bg="#2B2B2B", activebackground="#2B2B2B")
        root.config(bg="#2B2B2B")
        txt.config(text="Dark Mode: ON", bg="#2B2B2B")
        btnState = True


is_cancelled = False


def download_playlist(yt, stream, filelocation, count, total_video):
    global is_cancelled, file_size
    total_video = str(total_video)
    file_size = stream.filesize
    string = ''.join([i for i in re.findall('[\w +/.]', yt.title) if i.isalpha()])
    filename = filelocation + '/' + string + '.mp4'

    with open(filename, 'wb') as f:
        is_cancelled = False
        stream = request.stream(stream.url)
        downloaded = 0

        while True:
            download_video_button['state'] = 'disabled'
            download_audio_button['state'] = 'disabled'
            pbar["maximum"] = file_size
            pbar["value"] = downloaded
            pbar.start()
            if is_cancelled:
                progress_playlist['text'] = ''
                url_entry.delete(first=0, last="end")
                download_video_button['state'] = 'normal'
                download_audio_button['state'] = 'normal'
                choice.set("[--Video Quality--]")
                pbar.stop()
                pbar.grid_remove()
                messagebox.showinfo("Cancelled", "Video Download Cancelled!!!")
                return None
            chunk = next(stream, None)
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percentage = int((downloaded / file_size) * 100)
            else:
                # no more data
                progress['text'] = ''
                str(count)
                progress_playlist['text'] = f'Total video: {total_video}  Downloaded: {count}'
                print('Total video: ' + total_video + ' Downloaded: ', +count)
                count = int(count)
                count += 1
                return count


def checkDownloadable(flag):
    if flag is None:
        return True
    else:
        return False


def validate_link(checkurl):
    if '/playlist?' not in checkurl and '/watch?' not in checkurl:
        return True
    else:
        return False


def download_video(url, filelocation):
    global is_cancelled, file_size
    progress_playlist.grid_remove()
    download_video_button['state'] = 'normal'
    cancel_button['state'] = 'normal'

    if '/playlist?' in url:
        print('in playlist')
        progress_playlist.grid(row=6, column=0)
        progress_playlist['text'] = 'Connecting ...'
        playlist = selfPlaylist.Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        total_video = len(playlist.video_urls)
        print(f'Number of videos in playlist: {total_video}')
        count = 1

        for video_url in playlist.video_urls:
            pbar.grid(row=7, column=0, padx=20, sticky='nsew')
            flag = YouTube(video_url).streams.get_highest_resolution()
            if checkDownloadable(flag):
                url_entry.delete(first=0, last=1000)
                choice.set("[--Video Quality--]")
                download_video_button['state'] = 'normal'
                download_audio_button['state'] = 'normal'
                progress_playlist['text'] = ''
                tryagain = messagebox.askretrycancel("Couldn't Download",
                                                     "Some Youtube Videos Doesn't Have Permission To Download.\nTry Next Video?")
                if tryagain:
                    continue
                else:
                    url_entry.delete(first=0, last=1000)
                    choice.set("[--Video Quality--]")
                    download_video_button['state'] = 'normal'
                    download_audio_button['state'] = 'normal'
                    progress_playlist['text'] = ''
                    pbar.grid_remove()
                    return

            if choice.get() == '360p':
                try:
                    yt = YouTube(video_url)
                    stream = selfPlaylist.Playlist.VideoQuality('360p', yt)
                    file_size = stream.filesize
                except:
                    try:
                        yt = YouTube(video_url)
                        stream = selfPlaylist.Playlist.VideoQuality('480p', yt)
                        file_size = stream.filesize
                    except:
                        try:
                            yt = YouTube(video_url)
                            stream = selfPlaylist.Playlist.VideoQuality('720p', yt)
                            file_size = stream.filesize
                        except:
                            try:
                                yt = YouTube(video_url)
                                stream = selfPlaylist.Playlist.VideoQuality('1080p', yt)
                                file_size = stream.filesize
                            except:
                                url_entry.delete(first=0, last=1000)
                                choice.set("[--Video Quality--]")
                                download_video_button['state'] = 'normal'
                                download_audio_button['state'] = 'normal'
                                progress_playlist['text'] = ''
                                messagebox.showinfo("Quality Not Available", "Please select another quality")
                                return

            elif choice.get() == '480p':
                try:
                    yt = YouTube(video_url)
                    stream = selfPlaylist.Playlist.VideoQuality('480p', yt)
                    file_size = stream.filesize
                except:
                    try:
                        yt = YouTube(video_url)
                        stream = selfPlaylist.Playlist.VideoQuality('720p', yt)
                        file_size = stream.filesize
                    except:
                        try:
                            yt = YouTube(video_url)
                            stream = selfPlaylist.Playlist.VideoQuality('1080p', yt)
                            file_size = stream.filesize
                        except:
                            url_entry.delete(first=0, last=1000)
                            choice.set("[--Video Quality--]")
                            download_video_button['state'] = 'normal'
                            download_audio_button['state'] = 'normal'
                            progress_playlist['text'] = ''
                            messagebox.showinfo("Quality Not Available", "Please select another quality")
                            return

            elif choice.get() == '720p':
                try:
                    yt = YouTube(video_url)
                    stream = selfPlaylist.Playlist.VideoQuality('720p', yt)
                    # stream = yt.streams.get_highest_resolution()
                    file_size = stream.filesize
                except:
                    try:
                        yt = YouTube(video_url)
                        stream = selfPlaylist.Playlist.VideoQuality('480p', yt)
                        file_size = stream.filesize
                    except:
                        try:
                            yt = YouTube(video_url)
                            stream = selfPlaylist.Playlist.VideoQuality('360p', yt)
                            file_size = stream.filesize
                        except:
                            url_entry.delete(first=0, last=1000)
                            choice.set("[--Video Quality--]")
                            download_video_button['state'] = 'normal'
                            download_audio_button['state'] = 'normal'
                            progress_playlist['text'] = ''
                            messagebox.showinfo("Quality Not Available", "Please select another quality")
                            return

            elif choice.get() == '1080p':
                try:
                    yt = YouTube(video_url)
                    stream = selfPlaylist.Playlist.VideoQuality('1080p', yt)
                    file_size = stream.filesize
                except:
                    try:
                        yt = YouTube(video_url)
                        stream = selfPlaylist.Playlist.VideoQuality('720p', yt)
                        file_size = stream.filesize
                    except:
                        try:
                            yt = YouTube(video_url)
                            stream = selfPlaylist.Playlist.VideoQuality('480p', yt)
                            file_size = stream.filesize
                        except:
                            try:
                                yt = YouTube(video_url)
                                stream = selfPlaylist.Playlist.VideoQuality('360p', yt)
                                file_size = stream.filesize
                            except:
                                url_entry.delete(first=0, last=1000)
                                choice.set("[--Video Quality--]")
                                download_video_button['state'] = 'normal'
                                download_audio_button['state'] = 'normal'
                                progress_playlist['text'] = ''
                                messagebox.showinfo("Quality Not Available", "Please select another quality")
                                return

            count = download_playlist(yt, stream, filelocation, count, total_video)
            if count is None:
                return

        url_entry.delete(first=0, last=1000)
        choice.set("[--Video Quality--]")
        download_video_button['state'] = 'normal'
        download_audio_button['state'] = 'normal'
        progress_playlist['text'] = ''
        pbar.grid_remove()
        messagebox.showinfo("Done", "Full Playlist Download Completed!!!")

    elif '/watch?' in url:
        yt = YouTube(url)
        flag = yt.streams.get_highest_resolution()
        print('in video')
        progress['text'] = 'Connecting ...'
        if checkDownloadable(flag):
            url_entry.delete(first=0, last=1000)
            choice.set("[--Video Quality--]")
            download_video_button['state'] = 'normal'
            download_audio_button['state'] = 'normal'
            progress['text'] = ''
            messagebox.askretrycancel("Couldn't Download", "Some Youtube Videos Doesn't Have Permission To Download")
            return

        if choice.get() == '360p':
            if yt.streams.filter(file_extension='mp4', resolution='360p').first() is None:
                messagebox.showinfo("Quality Not Available", "Please select another quality")
                download_video_button['state'] = 'normal'
                download_audio_button['state'] = 'normal'
                progress['text'] = ''
                choice.set("[--Video Quality--]")
                return
            else:
                yt = YouTube(url)
                stream = selfPlaylist.Playlist.VideoQuality('360p', yt)

        elif choice.get() == '480p':
            if yt.streams.filter(file_extension='mp4', resolution='480p').first() is None:
                messagebox.showinfo("Quality Not Available", "Please select another quality")
                download_video_button['state'] = 'normal'
                download_audio_button['state'] = 'normal'
                progress['text'] = ''
                choice.set("[--Video Quality--]")
                return
            else:
                yt = YouTube(url)
                stream = selfPlaylist.Playlist.VideoQuality('480p', yt)

        elif choice.get() == '720p':
            if yt.streams.filter(file_extension='mp4', resolution='720p').first() is None:
                messagebox.showinfo("Quality Not Available", "Please select another quality")
                download_video_button['state'] = 'normal'
                download_audio_button['state'] = 'normal'
                progress['text'] = ''
                choice.set("[--Video Quality--]")
                return
            else:
                yt = YouTube(url)
                stream = selfPlaylist.Playlist.VideoQuality('720p', yt)

        elif choice.get() == '1080p':
            if yt.streams.filter(file_extension='mp4', resolution='1080p').first() is None:
                messagebox.showinfo("Quality Not Available", "Please select another quality")
                download_video_button['state'] = 'normal'
                download_audio_button['state'] = 'normal'
                progress['text'] = ''
                choice.set("[--Video Quality--]")
                return
            else:
                yt = YouTube(url)
                stream = selfPlaylist.Playlist.VideoQuality('1080p', yt)

        try:
            file_size = stream.filesize
        except:
            messagebox.showinfo("Quality Not Available", "Please select another quality")
            download_video_button['state'] = 'normal'
            download_audio_button['state'] = 'normal'
            progress['text'] = ''
            choice.set("[--Video Quality--]")
            return

        string = ''.join([i for i in re.findall('[\w +/.]', yt.title) if i.isalpha()])
        filename = filelocation + '/' + string + '.mp4'

        with open(filename, 'wb') as f:
            is_cancelled = False
            stream = request.stream(stream.url)
            downloaded = 0

            while True:
                pbar.grid(row=7, column=0, padx=20, sticky='nsew')
                download_video_button['state'] = 'disabled'
                download_audio_button['state'] = 'disabled'
                pbar["maximum"] = file_size
                pbar["value"] = downloaded
                pbar.start()
                if is_cancelled:
                    progress['text'] = ''
                    url_entry.delete(first=0, last="end")
                    download_video_button['state'] = 'normal'
                    download_audio_button['state'] = 'normal'
                    choice.set("[--Video Quality--]")
                    messagebox.showinfo("Cancelled", "Video Download Cancelled!!!")
                    pbar.stop()
                    pbar.grid_remove()
                    break
                chunk = next(stream, None)
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percentage = int((downloaded / file_size) * 100)
                    progress['text'] = f'Downloaded {percentage}%'
                else:
                    # no more data
                    url_entry.delete(first=0, last="end")
                    download_video_button['state'] = 'normal'
                    download_audio_button['state'] = 'normal'
                    progress['text'] = ''
                    choice.set("[--Video Quality--]")
                    pbar.grid_remove()
                    messagebox.showinfo("Done", "Video Download Completed!!!")
                    break
        print('done')


def download_audio(url, filelocation):
    global is_cancelled, file_size
    progress_playlist.grid_remove()
    download_video_button['state'] = 'normal'
    cancel_button['state'] = 'normal'

    if '/playlist?' in url:
        progress_playlist.grid(row=6, column=0)
        progress_playlist['text'] = 'Connecting ...'
        playlist = selfPlaylist.Playlist(url)
        total_video = len(playlist.video_urls)
        print('Number of audios in playlist: %s' % total_video)
        count = 1

        for video_url in playlist.video_urls:
            yt = YouTube(video_url)
            stream = yt.streams.filter(only_audio=True).first()
            count = download_playlist(yt, stream, filelocation, count, total_video)
            if count is None:
                return

        url_entry.delete(first=0, last=1000)
        choice.set("[--Video Quality--]")
        download_video_button['state'] = 'normal'
        download_audio_button['state'] = 'normal'
        progress_playlist['text'] = ''
        pbar.grid_remove()
        messagebox.showinfo("Done", "Full Playlist Download Completed!!!")

    elif '/watch?' in url:
        yt = YouTube(url)
        print('in audio')
        progress['text'] = 'Connecting ...'

        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        file_size = stream.filesize
        string = ''.join([i for i in re.findall('[\w +/.]', yt.title) if i.isalpha()])
        filename = filelocation + '/' + string + '.mp4'

        with open(filename, 'wb') as f:
            is_cancelled = False
            stream = request.stream(stream.url)
            downloaded = 0

            while True:
                download_video_button['state'] = 'disabled'
                download_audio_button['state'] = 'disabled'
                pbar["maximum"] = file_size
                pbar["value"] = downloaded
                pbar.start()
                if is_cancelled:
                    progress['text'] = ''
                    url_entry.delete(first=0, last="end")
                    download_video_button['state'] = 'normal'
                    download_audio_button['state'] = 'normal'
                    choice.set("[--Video Quality--]")
                    pbar.grid_remove()
                    messagebox.showinfo("Cancelled", "Video Download Cancelled!!!")
                    pbar.stop()
                    break
                chunk = next(stream, None)
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percentage = int((downloaded / file_size) * 100)
                    progress['text'] = f'Downloaded {percentage}%'
                else:
                    # no more data
                    url_entry.delete(first=0, last="end")
                    download_video_button['state'] = 'normal'
                    download_audio_button['state'] = 'normal'
                    progress['text'] = ''
                    choice.set("[--Video Quality--]")
                    pbar.grid_remove()
                    messagebox.showinfo("Done", "Video Download Completed!!!")
                    break
        print('done')


def start_video_download():
    link = url_entry.get()
    if validate_link(link):
        url_entry.delete(first=0, last="end")
        download_video_button['state'] = 'normal'
        download_audio_button['state'] = 'normal'
        progress['text'] = ''
        choice.set("[--Video Quality--]")
        messagebox.showerror("Invalid", "Please Enter Valid Link!!!")
        return

    if choice.get() == '[--Video Quality--]':
        messagebox.showerror("Invalid", "Please Select Video Quality!!!")
        return

    filelocation = askdirectory()
    threading.Thread(target=download_video, args=(url_entry.get(), filelocation), daemon=True).start()


def start_audio_download():
    link = url_entry.get()
    if validate_link(link):
        url_entry.delete(first=0, last="end")
        download_video_button['state'] = 'normal'
        download_audio_button['state'] = 'normal'
        progress['text'] = ''
        choice.set("[--Video Quality--]")
        messagebox.showerror("Invalid", "Please Enter Valid Link!!!")
        return

    filelocation = askdirectory()
    threading.Thread(target=download_audio, args=(url_entry.get(), filelocation), daemon=True).start()


def toggle_download():
    global is_paused
    is_paused = not is_paused
    # pause_button['text'] = 'Resume' if is_paused else 'Pause'


def cancel_download():
    global is_cancelled
    is_cancelled = True


# gui
root = Tk()
root.title("Friends Video Downloader")
root.iconbitmap("main img/Icon1.ico")
root.geometry("375x515+760+250")
root.resizable(False, False)

# switch toggle:
btnState = False

# switch images:
onImg = PhotoImage(file="dark img/switch-on.png")
offImg = PhotoImage(file="dark img/switch-off.png")

# Copyright
# originalBtn = Button(root, text="Made by Nishad", font="Rockwell", relief="flat")
# originalBtn.pack(side=BOTTOM)

# Night Mode:
txt = Label(root, text="Dark Mode: OFF", font="FixedSys 16", bg="#f0f0f0", fg="green")
txt.grid(row=11, column=0)

# switch widget:
btn = Button(root, text="OFF", borderwidth=0, command=dark_mode, bg="#f0f0f0", activebackground="#f0f0f0", pady=1)
btn.grid(row=0, column=0, sticky=NW)
btn.config(image=offImg)

# main icon section
file = PhotoImage(file="main img/rsz_check.png")
headingIcon = Label(root, image=file)
headingIcon.grid(row=0, column=0, pady=3)

# show info
txt1 = Label(root, text="Enter video/playlist link here:", font="FixedSys 16", bg="#f0f0f0", fg="black")
txt1.grid(row=1, column=0, sticky=W, padx=28, pady=0)

# Url Field
url_entry = Entry(root, justify=CENTER, bd=5, fg='green', width=57)
url_entry.grid(row=2, column=0, padx=10)
url_entry.focus()

# Select Quality
txt1 = Label(root, text="Select Quality:", font="FixedSys 16", bg="#f0f0f0", fg="black")
txt1.grid(row=3, column=0, sticky=W, padx=28, pady=10)

# test
choice = StringVar(root)
choice.set("[--Video Quality--]")  # default value

w = OptionMenu(root, choice, "360p", "480p", "720p", "1080p")
w["menu"].config(bg="#abd5ff", fg='black')
w.config(width=22, bg='#abd5ff', fg='black')
w.grid(row=3, column=0, sticky=E, padx=28, pady=10)

# Download Video Button
download_video_button = Button(root, text='Download Video', width=15, command=start_video_download, font='verdana',
                               relief='ridge', bd=5, bg='#028229', fg='white')
download_video_button.grid(row=4, column=0, pady=10)

# Download Audio Button
download_audio_button = Button(root, text='Download Audio', width=15, command=start_audio_download, font='verdana',
                               relief='ridge', bd=5, bg='#028229', fg='white')
download_audio_button.grid(row=5, column=0, pady=7)

# Progress
progress = Label(root)
# progress.pack(side=TOP)
progress.grid(row=6, column=0)
# progress.grid_forget()

progress_playlist = Label(root)
progress_playlist.grid(row=6, column=0)

# progrss_bar
pbar = ttk.Progressbar(root, orient="horizontal", length=file_size, mode="determinate")
pbar.grid(row=7, column=0, padx=20, sticky='nsew')
pbar.tkraise()
pbar.grid_remove()

# Cancel Button
cancel_button = Button(root, text='Cancel', width=10, command=cancel_download, state='disabled', font='verdana',
                       relief='ridge', bd=5, bg='white', fg='red')
cancel_button.grid(row=8, column=0, pady=20)

root.mainloop()
