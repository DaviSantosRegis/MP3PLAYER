from collections import OrderedDict
from utils import DICT
import musiclib
from pathlib import Path
import os
import sys
from numpy import array
from pygame import *
import json
from pprint import pprint
import codecs
import re
import time

os.system('cls')

Log = []
class Ev():
    def __init__(self):
        
        self.get = None
        self.mouse_pos = mouse.get_pos()
        for self.get in event.get():
            pass

        if self.Done(QUIT):
            sys.exit()

    def Done(self,EvType):

        if self.get != None:
            if self.get.type == EvType:
                Log.append({'ev':self.get,'time':time.time()})
                return True
        

src = Path() / 'src'

music_folder = src / 'MP3'
app_images = src / 'AppImages'
 
class App():
    def __init__(self):
        self.Input_Url()
        self.Player()
    
    def Input_Url(self):
        
        while True:
            l_saved_musics = len(list(music_folder.iterdir()))

            text = f"Input url Link: {'(Leave blank to acess saved musics) ' if l_saved_musics != 0 else ''}"
            link = input(text)
            
            if link == "":
                if l_saved_musics != 0:
                    break
            else:
                musiclib.YT.Downloader(link,music_folder).download()
                
    
    def Player(self):    
        MP3_Player()
        
class MP3_Player():
    def __init__(self):
        global mp3player,Width,Height,canvas
        
        mp3player = musiclib.MP3_Player(music_folder)
        
        Width = 300
        Height = Width + 55
        canvas = display.set_mode((Width,Height))
        self.player()

    def player(self):

        play_image = image.load(app_images / 'play.png')
        pause_image = image.load(app_images / 'pause.png')
        next_image = image.load(app_images / 'skip.png')
        previous_image = transform.rotate(next_image, 180)
        order_music_image = image.load(app_images / 'order_music.png')
        fonte = font.SysFont('calibri', 20)

        while True:
            ev = Ev()
            mp3player.update()
            canvas.fill([0]*3)
            #Loading Title of the music
            
            music_json = mp3player.Data.json
            title = f"{music_json['music']['name']} | {music_json['author']['name']}"  
            display.set_caption(title)
            
            #Loading The display 
            canvas.blit(mp3player.Data.img,(0,0))
            
            perc = mp3player.Music.Running_Time / mp3player.Music.Total_Time
            ProgressBar = draw.rect(canvas, [255,0,0], [0,Width,Width,5])
            draw.rect(canvas, [0,255,0], [*ProgressBar.topleft,Width*perc,5])
            
            if ProgressBar.collidepoint(ev.mouse_pos):
                if ev.Done(MOUSEBUTTONUP):
                    wperc = ev.mouse_pos[0] /ProgressBar.w
                    pos = wperc * mp3player.Music.Total_Time
                    mp3player.Music.set_pos(pos)
            
            RunState_image = play_image if mp3player.Music.RunningState else pause_image
            
            RunState = canvas.blit(RunState_image,
            ((ProgressBar.w - RunState_image.get_width())/2,ProgressBar.bottom)
            )

            Next = canvas.blit(next_image, RunState.topright)
            Previous = canvas.blit(previous_image, [RunState.topleft[0] - previous_image.get_width(),RunState.topleft[1]])
            
            
            

            ph_curr_n_music = draw.rect(canvas,[0]*3,[*ProgressBar.bottomleft,*Previous.bottomleft])      
            curr_n_music_text = f"{mp3player.Music.index + 1}/{mp3player.Music.l_PlaylistId}"
            curr_n_music_rect = fonte.render(curr_n_music_text, True, [255]*3)

            canvas.blit(curr_n_music_rect,
                                    array(ph_curr_n_music.center) - array(curr_n_music_rect.get_rect().center)
                        )

            ph_order_music = draw.rect(canvas, [0]*3, [*Next.topright,*canvas.get_rect().bottomright])
            
            
            
            Order_Music = canvas.blit(order_music_image, 
                            array(ph_order_music.center) - array(order_music_image.get_rect().center)
                            )          
            
            if ev.Done(MOUSEBUTTONUP):

                if RunState.collidepoint(ev.mouse_pos):
                    mp3player.Music.pause_unpause()

                if Next.collidepoint(ev.mouse_pos):
                    mp3player.Music.next()
                
                if Previous.collidepoint(ev.mouse_pos):
                    mp3player.Music.previous()

                if Order_Music.collidepoint(ev.mouse_pos):
                    self.order_music() 
                
                
            if ev.Done(KEYUP):
                # Previous - Next Music
                if ev.get.key == K_LEFT:
                    mp3player.Music.previous()

                if ev.get.key == K_RIGHT:
                    mp3player.Music.next()

                #Restart Music
                if ev.get.key == K_r:
                    mp3player.Music.restart()

                # Add segs to Music 
                time_skip = 5
                if ev.get.key == K_e:
                    
                    if mp3player.Music.Running_Time < time_skip:
                        mp3player.Music.restart()
                    
                    else:
                        mp3player.Music.set_pos(mp3player.Music.Running_Time - time_skip)                
                if ev.get.key == K_t:
                    mp3player.Music.set_pos(mp3player.Music.Running_Time + 5)

                #Pause Music
                if ev.get.key == K_SPACE:
                    mp3player.Music.pause_unpause()
            display.update()
        
    def order_music(self):
        
        

        

        preview_playlist_data = {}
        for _id in mp3player.Music.PlaylistId:
            _img = image.load(_id / 'thumb.jpg')
            _img = transform.smoothscale(_img, (35,35))
            
            with codecs.open(_id/'data.json',encoding='utf-8') as fp:
                _json = json.load(fp)
            
            preview_playlist_data[_id] = {'img':_img,'json':_json}

        
        
        

        fonte_title = font.SysFont('calibri', 15)
        fonte_artist = font.SysFont('calibri', 13)
        fonte_viewsCount = fonte_artist
        fonte_Seconds = font.SysFont('calibri', 12)
        
        Scroll = 0
        ReverseOrd = False
        Keys = None
        while True:
            ev = Ev()
            key_get_pressed = key.get_pressed()

            music_json = mp3player.Data.json
            title = f"{music_json['music']['name']} | {music_json['author']['name']}"  
            display.set_caption(title)

            canvas.fill(0)
            mp3player.update()

            

            if ev.Done(MOUSEBUTTONUP):
                if curr_music_blit.collidepoint(ev.mouse_pos):
                    self.player()
            


            for i,_id in enumerate(preview_playlist_data):
                _id_data = preview_playlist_data[_id]


                ph_color = [30]*3 if i % 2 == 0 else [50]*3
                ph_music_h = 50
                ph_music = draw.rect(canvas, ph_color, [0,i*50 + Scroll,Width,ph_music_h])
                
                
                ph_music_img = draw.rect(canvas, ph_color, [*ph_music.topleft,ph_music.h,ph_music.h])
                music_img = _id_data['img']
                
                music_img_blit = canvas.blit(music_img,
                                array(ph_music_img.center) - array(music_img.get_rect().center)
                                )
                
                music_title_text = _id_data['json']['music']['name']
                music_artist_text = _id_data['json']['author']['name']
                music_viewsCount_text = ' {0:,}'.format(int(_id_data['json']['music']['viewsCount'])).replace(',', '.')
                music_durationSeg_text = time.strftime(
                                                "%M:%S",
                                                time.gmtime(
                                                            int(_id_data['json']['music']['lenghtSeconds'])
                                                           )
                                                    )

                music_title_rect = fonte_title.render(music_title_text, True, [255]*3)
                music_title_blit = canvas.blit(music_title_rect, array(music_img_blit.topright) + array([5,0]))                

                
                music_artist_rect = fonte_artist.render(music_artist_text, True, [255]*3)
                music_artist_blit = canvas.blit(music_artist_rect, array(music_title_blit.bottomleft))
                
                

                
                music_viewsCount_rect = fonte_viewsCount.render(music_viewsCount_text, True, [255]*3)
                music_viewsCount_blit = canvas.blit(music_viewsCount_rect, array(music_artist_blit.topright) + array([5,0])) 
            

                music_durationSeg_rect = fonte_Seconds.render(music_durationSeg_text, True, [255]*3)
                music_durationSeg_blit = canvas.blit(music_durationSeg_rect, 
                                                    array(ph_music.bottomright) - array(music_durationSeg_rect.get_size())
                            )
                

                
                
                
                if mp3player.Music.index == i:
                    surfRunning = Surface(ph_music.size)
                    surfRunning.set_alpha(150)
                    canvas.blit(surfRunning,ph_music)
                    
                height_menu = 64
                curr_music_img = transform.smoothscale(mp3player.Data.img,[height_menu]*2)
                curr_music_blit = canvas.blit(curr_music_img, 
                                                            (Width - height_menu,Height - height_menu))
                
                N = (-ph_music_h * mp3player.Music.l_PlaylistId) + Height
                
                
                if ev.Done(MOUSEWHEEL):
                    Scroll += ev.get.y 
                    
                    if Scroll >= 0:    
                        Scroll = 0


                    if Scroll <= N:
                        Scroll = N
                
                

                
                if key_get_pressed[K_UP]:
                    if Scroll >= 0:
                        Scroll = 0
                    else:
                        Scroll += 1
                    
                if key_get_pressed[K_DOWN]:
                    if Scroll <= N:
                        Scroll = N
                    else:
                        Scroll -= 0.5


                    
                
                if ev.Done(MOUSEBUTTONUP):
                    
                    if ev.get.button == 1:       
                        if music_img_blit.collidepoint(ev.mouse_pos):
                            
                            mp3player.Music.PlaylistId = list(preview_playlist_data.keys())
                            mp3player.Music.set_music(i)
                    
                    
                    if ev.get.button == 3:
                        blits = [music_title_blit,music_artist_blit,music_viewsCount_blit,music_durationSeg_blit]
                        CldAnyAText = any([blit.collidepoint(ev.mouse_pos) for blit in blits])
                        
                        
                        
                        if CldAnyAText:
                            if ReverseOrd:
                                ReverseOrd = False
                            else:
                                ReverseOrd = True
                            if music_title_blit.collidepoint(ev.mouse_pos):
                                Keys = ['json','music','name']
                            if music_artist_blit.collidepoint(ev.mouse_pos):
                                Keys = ['json','author','name']
                            
                            if music_viewsCount_blit.collidepoint(ev.mouse_pos):
                                Keys = ['json','music','viewsCount']
                                
                            if music_durationSeg_blit.collidepoint(ev.mouse_pos):
                                Keys = ['json','music','lenghtSeconds']

                           

                        preview_playlist_data = DICT(preview_playlist_data).SortBy(Keys,ReverseOrd)
                        mp3player.Music.PlaylistId = list(preview_playlist_data.keys()) 
                        mp3player.Music.index = mp3player.Music.PlaylistId.index(mp3player.Music.id)
                        

                    
                    
                        

            
                   
                    
                    
                            
                        
                        
                            


                    
            
                    
                    
            display.update()

    
App()
        

    