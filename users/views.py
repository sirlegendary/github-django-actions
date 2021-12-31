from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.forms import CustomUserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.conf import settings
import os

from users.models import Board, BoardText, StickyNotes, Url, Image, Video

def dashboard(request):
    current_user_id = request.user.id
    boards = Board.objects.filter(user_id=current_user_id).order_by('-created')
    stuff_for_frontend = {
        'boards': boards if len(boards) > 0 else None
    }
    return render(request, "users/dashboard.html", stuff_for_frontend)

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )

def create_board(request):
    current_user_id = request.user.id
    
    if request.method == "POST":
        title = request.POST.get('title')

        if len(title) == 0 or title.isspace():
            stuff_for_frontend = {
                'error_message': "You have to fill out all fields.",
            }
            return render(request, 'users/create_board.html', stuff_for_frontend)
        else:
            board = Board.objects.create(title=title, user_id=current_user_id)
            board.save()
            return HttpResponseRedirect(reverse('dashboard'))

    else:
        return render(request, "users/create_board.html")

def edit_board(request, board_id):

    if request.method == "POST":
        title = request.POST.get('title')

        if len(title) == 0 or title.isspace():
            board = Board.objects.filter(id=board_id)
            stuff_for_frontend = {
                'error_message': "You have to fill out all fields.",
                'board': board
            }
            return render(request, 'users/create_board.html', stuff_for_frontend)
        else:
            try:
                #Update database
                Board.objects.filter(id=board_id).update(title=title, updated=timezone.now())

                boards = Board.objects.filter(user_id=request.user.id).order_by('-created')
                stuff_for_frontend = {
                    'success_message': '{} - Board has been successfully Updated.'.format(title),
                    'boards': boards if len(boards) > 0 else None
                }
                encoded_string = urllib.urlencode(my_dict)
                redirect('/dashboard/?%s'%encoded_string)
                # return render(request, "users/dashboard.html", stuff_for_frontend)
            except:
                board = Board.objects.filter(id=board_id)
                stuff_for_frontend = {
                    'error_message': "Could not update database.",
                    'board': board
                }
                return render(request, 'users/create_board.html', stuff_for_frontend)

    else:
        board = Board.objects.filter(id=board_id)
        stuff_for_frontend = {
            'board': board
        }
        return render(request, "users/create_board.html", stuff_for_frontend)

def delete_board(request, board_id):
    boards = Board.objects.filter(user_id=request.user.id).order_by('-created')

    try:
        board = get_object_or_404(Board, id=board_id)
        board.delete()
        
        stuff_for_frontend = {
            'boards': boards if len(boards) > 0 else None,
            'success_message': 'Board has been successfully deleted.'
        }
        return render(request, "users/dashboard.html", stuff_for_frontend)
    except:
        stuff_for_frontend = {
            'boards': boards if len(boards) > 0 else None,
            'error_message': 'Could not delete board, please try again later.'
        }
        return render(request, "users/dashboard.html", stuff_for_frontend)

        

def board(request, board_id):

    stuff_for_frontend = query_all_tables(board_id)
    return render(request, "users/board.html", stuff_for_frontend)

def create_board_text(request, board_id):

    if request.method == "POST":
        text = request.POST.get('board_text')

        if len(text) == 0 or text.isspace():
            stuff_for_frontend = {
                'error_message': "Please add text.",
                'board_id': board_id
            }
            return render(request, 'users/create_board_text.html', stuff_for_frontend)
        else:
            boardtext = BoardText.objects.create(
                text=text, 
                board=Board.objects.get(id=board_id)
            )
            boardtext.save()
            stuff_for_frontend = query_all_tables(board_id)
            return render(request, 'users/board.html', stuff_for_frontend)
            # return HttpResponseRedirect(reverse('board', kwargs=stuff_for_frontend))
    else:
        stuff_for_frontend = {
            'board_id': board_id
        }
        return render(request, 'users/create_board_text.html', stuff_for_frontend)


def create_url(request, board_id):

    if request.method == "POST":
        title = request.POST.get('title')
        url   = request.POST.get('url')

        if len(title) == 0 or title.isspace() or len(url) == 0 or url.isspace():
            stuff_for_frontend = {
                'error_message': "Please fill out all fields.",
                'board_id': board_id
            }
            return render(request, 'users/create_url.html', stuff_for_frontend)
        else:
            url = Url.objects.create(
                title=title,
                url=url, 
                board=Board.objects.get(id=board_id)
            )
            url.save()
            stuff_for_frontend = query_all_tables(board_id)
            return render(request, 'users/board.html', stuff_for_frontend)
    else:
        stuff_for_frontend = {
            'board_id': board_id
        }
        return render(request, 'users/create_url.html', stuff_for_frontend)

def create_sticky_note(request, board_id):

    if request.method == "POST":
        note = request.POST.get('note')

        if len(note) == 0 or note.isspace():
            stuff_for_frontend = {
                'error_message': "Please do not submit an empty field.",
                'board_id': board_id
            }
            return render(request, 'users/create_sticky_note.html', stuff_for_frontend)
        else:
            note = StickyNotes.objects.create(
                note=note, 
                board=Board.objects.get(id=board_id)
            )
            note.save()
            stuff_for_frontend = query_all_tables(board_id)
            return render(request, 'users/board.html', stuff_for_frontend)
    else:
        stuff_for_frontend = {
            'board_id': board_id
        }
        return render(request, 'users/create_sticky_note.html', stuff_for_frontend)

def upload_image(request, board_id): #https://www.geeksforgeeks.org/python-uploading-images-in-django/
    if request.method == "POST":
        img = request.FILES['image']
        stuff_for_frontend = query_all_tables(board_id)
        try:
            img = Image.objects.create(
                image=img,
                board=Board.objects.get(id=board_id)
            )
            img.save()
            stuff_for_frontend['success_message'] = 'Image Uploaded.'
        except:
            stuff_for_frontend['error_message'] = 'Something went wrong. Please try again later.'
       
        return render(request, 'users/board.html', stuff_for_frontend)
    else:
        stuff_for_frontend = {
            'board_id': board_id
        }
        return render(request, 'users/upload_image.html', stuff_for_frontend)

def upload_video(request, board_id):
    if request.method == "POST":
        vid = request.FILES['video']
        stuff_for_frontend = query_all_tables(board_id)
        try:
            vid_obj = Video.objects.create(
                video=vid,
                board=Board.objects.get(id=board_id)
            )
            vid_obj.save()
            stuff_for_frontend['success_message'] = 'Video Uploaded.'
        except:
            stuff_for_frontend['error_message'] = 'Something went wrong. Please try again later.'
       
        return render(request, 'users/board.html', stuff_for_frontend)
    else:
        stuff_for_frontend = {
            'board_id': board_id
        }
        return render(request, 'users/upload_video.html', stuff_for_frontend)

def delete_board_text(request, board_text_id):
    board_item = "Text"

    try:
        board_text_object = BoardText.objects.get(id=board_text_id)
        board_id = board_text_object.board.id
   
        stuff_for_frontend = delete_board_items(request, board_item, board_text_id, board_id)
   
        return render(request, "users/board.html", stuff_for_frontend)
    except:
        return HttpResponseRedirect(reverse('dashboard'))

def delete_url(request, url_id):
    board_item = "URL"

    try:
        url_object = Url.objects.get(id=url_id)
        board_id = url_object.board.id
   
        stuff_for_frontend = delete_board_items(request, board_item, url_id, board_id)
   
        return render(request, "users/board.html", stuff_for_frontend)
    except:
        return HttpResponseRedirect(reverse('dashboard'))

def delete_sticky_note(request, note_id):
    board_item = "Sticky Note"

    try:
        note_object = StickyNotes.objects.get(id=note_id)
        board_id = note_object.board.id
   
        stuff_for_frontend = delete_board_items(request, board_item, note_id, board_id)
   
        return render(request, "users/board.html", stuff_for_frontend)
    except:
        return HttpResponseRedirect(reverse('dashboard'))


def delete_image(request, image_id):
    board_item = "Image"

    try:
        image_object = Image.objects.get(id=image_id)
        board_id = image_object.board.id
   
        stuff_for_frontend = delete_board_items(request, board_item, image_id, board_id)
   
        return render(request, "users/board.html", stuff_for_frontend)
    except:
        return HttpResponseRedirect(reverse('dashboard'))

def delete_video(request, video_id):
    board_item = "Video"

    try:
        video_object = Video.objects.get(id=video_id)
        board_id = video_object.board.id
   
        stuff_for_frontend = delete_board_items(request, board_item, video_id, board_id)
   
        return render(request, "users/board.html", stuff_for_frontend)
    except:
        return HttpResponseRedirect(reverse('dashboard'))

def delete_board_items(request, board_item, board_item_id, board_id):
    
    try:
        if board_item == 'Text':
            BoardText.objects.filter(id=board_item_id).delete()
        elif board_item == 'URL':
            Url.objects.filter(id=board_item_id).delete()
        elif board_item == 'Sticky Note':
            StickyNotes.objects.filter(id=board_item_id).delete()
        elif board_item == 'Image':
            image_obj = Image.objects.get(id=board_item_id)
            image_path = image_obj.image
            Image.objects.filter(id=board_item_id).delete()
            os.remove(os.path.join(settings.MEDIA_ROOT, str(image_path)))
        elif board_item == 'Video':
            video_obj = Video.objects.get(id=board_item_id)
            video_path = video_obj.video
            Video.objects.filter(id=board_item_id).delete()
            os.remove(os.path.join(settings.MEDIA_ROOT, str(video_path)))
        
        
        stuff_for_frontend = query_all_tables(board_id)
        stuff_for_frontend['success_message'] = board_item + ' was successfully deleted.'
        
        return stuff_for_frontend
    except:
        stuff_for_frontend = query_all_tables(board_id)
        stuff_for_frontend['error_message'] = 'Could not delete ' + board_item

        return stuff_for_frontend

def edit_board_text(request, bt_id):
    board_text_object = BoardText.objects.get(id=bt_id)
    board_id = board_text_object.board.id
    if request.method == "POST":
        board_text = request.POST.get('board_text')

        if len(board_text) == 0 or board_text.isspace():
            board_text = BoardText.objects.get(id=bt_id)
            stuff_for_frontend = {
                'error_message': "You have to fill out all fields.",
                'board_text': board_text,
                'board_id': board_id
            }
            return render(request, 'users/create_board_text.html', stuff_for_frontend)
        else:
            try:
                BoardText.objects.filter(id=bt_id).update(text=board_text, updated=timezone.now())
                stuff_for_frontend = query_all_tables(board_id)
                stuff_for_frontend['success_message'] = 'Board Text was successfully updated.'
                stuff_for_frontend['board_id'] = board_id
                return render(request, "users/board.html", stuff_for_frontend)
            except:
                board_text = BoardText.objects.get(id=bt_id)
                stuff_for_frontend = {
                    'error_message': "Could not update database.",
                    'board_text': board_text,
                    'board_id': board_id
                }
                return render(request, 'users/create_board_text.html', stuff_for_frontend)
    else:
        board_text = BoardText.objects.get(id=bt_id)
        stuff_for_frontend = {
            'board_text': board_text,
            'board_id': board_id
        }
        return render(request, 'users/create_board_text.html', stuff_for_frontend)

def edit_url(request, link_id):

    url_object = Url.objects.get(id=link_id)
    board_id = url_object.board.id
    if request.method == "POST":
        title = request.POST.get('title')
        url = request.POST.get('url')

        if len(title) == 0 or title.isspace() or len(url) == 0 or url.isspace():
            url = Url.objects.get(id=link_id)
            stuff_for_frontend = {
                'error_message': "You have to fill out all fields.",
                'url': url,
                'board_id': board_id
            }
            return render(request, 'users/create_url.html', stuff_for_frontend)
        else:
            try:
                Url.objects.filter(id=link_id).update(title=title, url=url, updated=timezone.now())
                stuff_for_frontend = query_all_tables(board_id)
                stuff_for_frontend['success_message'] = 'Url was successfully updated.'
                stuff_for_frontend['board_id'] = board_id
                return render(request, "users/board.html", stuff_for_frontend)
            except:
                url = Url.objects.get(id=link_id)
                stuff_for_frontend = {
                    'error_message': "Could not update database.",
                    'url': url,
                    'board_id': board_id
                }
                return render(request, 'users/create_url.html', stuff_for_frontend)
    else:
        url = Url.objects.get(id=link_id)
        stuff_for_frontend = {
            'url': url,
            'board_id': board_id
        }
        return render(request, 'users/create_url.html', stuff_for_frontend)

def edit_sticky_note(request, note_id):

    note_object = StickyNotes.objects.get(id=note_id)
    board_id = note_object.board.id
    if request.method == "POST":
        note = request.POST.get('note')

        if len(note) == 0 or note.isspace():
            note = StickyNotes.objects.get(id=note_id)
            stuff_for_frontend = {
                'error_message': "You have to fill out all fields.",
                'note': note,
                'board_id': board_id
            }
            return render(request, 'users/create_sticky_note.html', stuff_for_frontend)
        else:
            try:
                StickyNotes.objects.filter(id=note_id).update(note=note, updated=timezone.now())
                stuff_for_frontend = query_all_tables(board_id)
                stuff_for_frontend['success_message'] = 'Sticky Note was successfully updated.'
                stuff_for_frontend['board_id'] = board_id
                return render(request, "users/board.html", stuff_for_frontend)
            except:
                note = StickyNotes.objects.get(id=note_id)
                stuff_for_frontend = {
                    'error_message': "Could not update database.",
                    'note': note,
                    'board_id': board_id
                }
                return render(request, 'users/create_sticky_note.html', stuff_for_frontend)
    else:
        note = StickyNotes.objects.get(id=note_id)
        stuff_for_frontend = {
            'note': note,
            'board_id': board_id
        }
        return render(request, 'users/create_sticky_note.html', stuff_for_frontend)


def query_all_tables(board_id):
    board           = Board.objects.get(id=board_id)
    boardtexts      = BoardText.objects.filter(board=board_id).order_by('-created')
    notes           = StickyNotes.objects.filter(board=board_id).order_by('-created')
    url             = Url.objects.filter(board=board_id).order_by('-created')
    images          = Image.objects.filter(board=board_id).order_by('-created')
    videos          = Video.objects.filter(board=board_id).order_by('-created')
    
    result_set = {
        'board': board,
        'boardtexts': boardtexts,
        'notes':notes,
        'url':url,
        'images':images,
        'videos':videos
    }
    return result_set

# Always return an HttpResponseRedirect after successfully dealing
# with POST data. This prevents data from being posted twice if a
# user hits the Back button.
# return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))