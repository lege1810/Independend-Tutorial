from flask import Flask, render_template, send_from_directory, request, make_response, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from random import randint
import os
import base64
import gridfs
import bcrypt

client = MongoClient()
app = Flask(__name__, template_folder='templates')
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def newAllUsers():
    return{
        'users': [],
        'id': 'allUsers'
    }


def newAllCourses():
    return{
        'courses': [],
        'id': 'allCourses'
    }


def newEmptyUserCourse():
    return {
        'course':
        {
            'courseID': None
        }
    }


def newEmptyUser():
    return {
        'id': ObjectId(),
        'mail': None,
        'first_name': None,
        'last_name': None,
        'nickname': None,
        'passphrase': None,
        'isTutor': None,
        'courses': [],
        'ownCourses': [],
        'progress': newEmptyProgress()
    }


def newEmptyCourse():
    return {
        'id': ObjectId(),
        'name': None,
        'description': None,
        'courseBannerID': None,
        'courseDownloadDescription': None,
        'courseDownloads': [],
        'recap' : None,
        'categorys': {
            'documents': []},
    }

def newEmptyProgress():
    return {
        'answers': [],
        'downloads': [],
        'documents': []
    }


def newEmptyProgressItem():
    return {
        'foreignKey': None,
        'value': None
    }


def newCourseDownload():
    return {
        'fileID': None,
        'fileName': None
    }


def newDocument():
    return {
        'title': None,
        'id': ObjectId(),
        'styleTyp': None,
        'content': {
            'h1': [],
            'p': [],
            'courseImgID': None,
            'courseVideoID': None
        }
    }


def newRecap():
    return {
        'name': None,
        'questions': []
    }


def newQuestion():
    return {
        'questionText': None,
        'answers': []
    }


def newAnswer():
    return {
        'id': ObjectId(),
        'answerText': None,
        'answerIsCorrect': None
    }


def fillDB():
    # DB-Connection
    db = client.myTestBase
    # Collection
    studCorp = db.studCorp
    # ------Define new Users/Tutors-------
    singleExampleUser = newEmptyUser()
    singleExampleUser['id'] = 1
    singleExampleUser['mail'] = 'm.maart@gmx.net'
    singleExampleUser['first_name'] = 'Moritz'
    singleExampleUser['last_name'] = 'Maart'
    singleExampleUser['nickname'] = 'nordie92'
    singleExampleUser['passphrase'] = 'Okay123'
    singleExampleUser['isTutor'] = False

    singleExampleUser2 = newEmptyUser()
    singleExampleUser2['id'] = 2
    singleExampleUser2['mail'] = 'me.mail@web.net'
    singleExampleUser2['first_name'] = 'Me'
    singleExampleUser2['last_name'] = 'Muster'
    singleExampleUser2['nickname'] = 'spaceboi'
    singleExampleUser2['passphrase'] = 'Jauuuu111'
    singleExampleUser2['isTutor'] = False

    singleExampleTutor = newEmptyUser()
    singleExampleTutor['id'] = 3
    singleExampleTutor['mail'] = 'a.b@c.de'
    singleExampleTutor['first_name'] = 'Le'
    singleExampleTutor['last_name'] = 'Ge'
    singleExampleTutor['nickname'] = 'lege1810'
    singleExampleTutor['passphrase'] = '12345'
    singleExampleTutor['isTutor'] = True

    newCourse = newEmptyUserCourse()
    newCourse['course']['courseID'] = '1'

    newCourse2 = newEmptyUserCourse()
    newCourse2['course']['courseID'] = '2'

    singleExampleUser['courses'].append(newCourse)
    singleExampleUser2['courses'].append(newCourse2)
    singleExampleTutor['ownCourses'].append(newCourse)

    allUsers = newAllUsers()

    allUsers['users'].append(singleExampleUser)
    allUsers['users'].append(singleExampleUser2)
    allUsers['users'].append(singleExampleTutor)

    studCorp.insert(allUsers)
    # ------------------Define new Tutorial-----------------------------------
    newTutorial = newEmptyCourse()
    # newTutorial['id'] = '1234567890qwertzuio2'
    newTutorial['name'] = 'Web-Systeme'
    newTutorial['description'] = 'Lernen sie Technologien zu vergleichen'

    newDoc = newDocument()
    newDoc['title'] = 'TestPage1'
    newDoc['styleTyp'] = 1
    newDoc['content']['link'] = 'rel="stylesheet" href="./css/design1.css"'
    newDoc['content']['h1'].append('Überschrift1 Bla Bla Bla')
    newDoc['content']['p'].append(
        'Das ist alles ein Paragraph bla bla bla ... bla bla bla')

    # #öffne Grid-Fs-Collection
    # db = client.myTestBase
    # fsCollection = gridfs.GridFS(db)

    # #für Kurs Banner
    # bannerID = ObjectId()
    # newTut['courseBannerID'] = bannerID
    # fsCollection.put(courseBanner, filename = courseBanner.filename, _id = bannerID)

    newDoc_1 = newDocument()
    newDoc_1['title'] = 'TestPageNummer 2'
    newDoc_1['styleTyp'] = 2

    newDoc_1['content']['link'] = 'rel="stylesheet" href="./css/design2.css"'
    newDoc_1['content']['h1'].append('WAS GEHT AB ÜBERSCHRIFT')
    newDoc_1['content']['p'].append(
        'Beispiel Paragraph')

    newExampleQuiz = newQuiz()
    newExampleQuiz['name'] = 'Quiz 1'

    newExampleQuestion = newQuestion()
    newExampleQuestion['questionText'] = 'Ist der Himmel für uns blau?'

    newExampleAnswer = newAnswer()
    newExampleAnswer['answerText'] = 'Ja'
    newExampleAnswer['answerIsCorrect'] = True

    newExampleAnswer2 = newAnswer()
    newExampleAnswer2['answerText'] = 'Nein'
    newExampleAnswer2['answerIsCorrect'] = False

    newExampleQuestion['answers'].append(newExampleAnswer)
    newExampleQuestion['answers'].append(newExampleAnswer2)

    newExampleQuiz['questions'].append(newExampleQuestion)

    newTutorial['categorys']['quiz'].append(newExampleQuiz)
    newTutorial['categorys']['documents'].append(newDoc)
    newTutorial['categorys']['documents'].append(newDoc_1)

    allCourses = newAllCourses()
    allCourses['id'] = 'allCourses'
    allCourses['courses'].append(newTutorial)

    # -----------------------------
    newTutorial2 = newEmptyCourse()
    # newTutorial2['id'] = '1234567890qwertzuio'
    newTutorial2['name'] = 'Mathe'
    newTutorial2['description'] = 'Integrale'

    newDoc2 = newDocument()
    newDoc2['title'] = 'TestPage1'
    newDoc2['styleTyp'] = 1
    newDoc2['content']['link'] = 'rel="stylesheet" href="./css/design1.css"'
    newDoc2['content']['h1'].append('Überschrift1 Bla Bla Bla')
    newDoc2['content']['p'].append(
        'Das ist alles ein Paragraph bla bla bla ... bla bla bla')

    newExampleQuiz2 = newQuiz()
    newExampleQuiz2['name'] = 'Quiz 1'

    newExampleQuestion2 = newQuestion()
    newExampleQuestion2['questionText'] = 'Ist der Himmel für uns blau?'

    newExampleAnswer2_1 = newAnswer()
    newExampleAnswer2_1['answerText'] = 'Ja'
    newExampleAnswer2_1['answerIsCorrect'] = True

    newExampleAnswer2_2 = newAnswer()
    newExampleAnswer2_2['answerText'] = 'Nein'
    newExampleAnswer2_2['answerIsCorrect'] = False

    newExampleQuestion2['answers'].append(newExampleAnswer2_1)
    newExampleQuestion2['answers'].append(newExampleAnswer2_2)

    newExampleQuiz2['questions'].append(newExampleQuestion2)

    newTutorial2['categorys']['quiz'].append(newExampleQuiz2)
    newTutorial2['categorys']['documents'].append(newDoc2)

    allCourses['courses'].append(newTutorial2)
    studCorp.insert(allCourses)


def initDB():
    # DB-Connection
    db = client.myTestBase
    # Collection
    studCorp = db.studCorp
    allCourses = newAllCourses()
    allUsers = newAllUsers()

    studCorp.insert(allUsers)
    studCorp.insert(allCourses)


def getCollection():
    # DB-Connection
    db = client.myTestBase
    # Collection
    studCorp = db.studCorp
    return studCorp.find()


def deleteCollection():
    # DB-Connection
    db = client.myTestBase
    # Collection
    studCorp = db.studCorp
    gridFsFiles = db.fs.files
    gridFsChunks = db.fs.chunks
    db.drop_collection(gridFsFiles)
    db.drop_collection(gridFsChunks)
    db.drop_collection(studCorp)


def getAllUsersWrapperObject():
    db = client.myTestBase
    studCorp = db.studCorp
    fullDB = studCorp.find()
    return fullDB[0]

# get all users
def getAllUsers():
    db = client.myTestBase
    studCorp = db.studCorp
    fullDB = studCorp.find()
    return fullDB[0]['users']


def getUserByMail(mail):
    users = getAllUsers()
    user = next((x for x in users if x['mail'] == mail), None)
    return user


# get user by cookieID
def getUser(cookieID):
    allUsers = getAllUsers()
    foundUser = {}
    for user in allUsers:
        if user['id'] == cookieID:
            foundUser = user
            break
    return foundUser


def getNicknameIfExists():
    if 'nickname' in session:
        return session['nickname']
    else:
        return ''


def updateUserData(mail, newUser):
    allUsers = getAllUsersWrapperObject()
    for user in allUsers['users']:
        if user['mail'] == mail:
            user = newUser
            break
    updateDataBase('allUsers', allUsers)


# checking if user already exits by comparing mail
def userExists(mail):
    users = getAllUsers()
    user = next((x for x in users if x['mail'] == mail), None)
    return user is not None


def getUser(cookieID):
    allUsers = getAllUsers()
    foundUser = {}
    for user in allUsers:
        if user['id'] == cookieID:
            foundUser = user
            break
    return foundUser


# checking if user is logged in
def isLoggedIn():
    return 'mail' in session


def getAllCoursesWrapperObject():
    db = client.myTestBase
    studCorp = db.studCorp
    fullDB = studCorp.find()
    return fullDB[1]


def getAllCourses():
    db = client.myTestBase
    studCorp = db.studCorp
    fullDB = studCorp.find()
    return fullDB[1]['courses']


def getCourse(courseID):
    allCourses = getAllCourses()
    foundcourse = None
    for course in allCourses:
        if course['id'] == courseID:
            foundcourse = course
            break

    return foundcourse


def getCourseWithString(courseID):
    allCourses = getAllCourses()
    foundcourse = None
    for course in allCourses:
        if str(course['id']) == courseID:
            foundcourse = course
            break

    return foundcourse


def getCourseIndex(courseID):
    allCourses = getAllCourses()
    courseIndex = 0
    for course in allCourses:
        if str(course['id']) != courseID:
            courseIndex += 1
        else:
            break

    if courseIndex >= len(allCourses):
        print("Fehler in getCourseIndex: Index out of range")

    return courseIndex


def updateDataBase(whatToUpdate, document):
    db = client.myTestBase
    studCorp = db.studCorp
    try:
        docSelector = {"id": whatToUpdate}
        studCorp.update_one(docSelector, {"$set": document})
    except Exception:
        print("Fehler in UpdateDataBase, Dokument zum updaten nicht gefunden.")


def getDocumentIndex(documentID, course):
    foundIndex = 0
    for documents in course['categorys']['documents']:
        if str(documents['id']) == documentID:
            break
        foundIndex += 1
    if foundIndex >= len(course['categorys']['documents']):
        foundIndex = 0
    return foundIndex


def renderTutorialTemplate(course, documentIndex, documentImgID, documentVideoID):
    # Unterscheidung des Template Styles
    templateToRender = None
    if int(course['categorys']['documents'][documentIndex]['styleTyp']) == 1:
        if isLoggedIn():
            templateToRender = render_template('tutorialStyle1.html',
                username=getNicknameIfExists(),
                userLogged=True,
                course=course,
                documentIndex=documentIndex,
                documentVideoID=documentVideoID,
                userIsCourseMember = isCourseMember(getUserFromSession()['id'], course['id']),
                userIsCourseOwner = isCourseOwner(getUserFromSession()['id'], course['id']))
        else:
            templateToRender = render_template('tutorialStyle1.html',
                username=getNicknameIfExists(),
                userLogged=False,
                course=course,
                documentIndex=documentIndex,
                documentVideoID=documentVideoID)
    else:
        if isLoggedIn():
            templateToRender = render_template('tutorialStyle2.html',
                username=getNicknameIfExists(),
                userLogged=True,
                course=course,
                documentIndex=documentIndex,
                documentImgID=documentImgID,
                userIsCourseMember = isCourseMember(getUserFromSession()['id'], course['id']),
                userIsCourseOwner = isCourseOwner(getUserFromSession()['id'], course['id']))
        else:
            templateToRender = render_template('tutorialStyle2.html',
                username=getNicknameIfExists(),
                userLogged=False,
                course=course,
                documentIndex=documentIndex,
                documentImgID=documentImgID)

    return templateToRender


# Liefert die ersten 6 Kurse
def getIndexTutorials(course):
    requiredCourses = {
        'Satz0': [],
        'Satz1': []
    }
    for i in range(0, 6):
        if i < 3:
            if i < len(course):
                requiredCourses['Satz0'].append(course[i])
            else:
                requiredCourses['Satz0'].append(newEmptyCourse())
        else:
            if i < len(course):
                requiredCourses['Satz1'].append(course[i])
            else:
                requiredCourses['Satz1'].append(newEmptyCourse())
    return requiredCourses


def getCourseIfExists(courseID):
    course = None
    if courseID is not None:
        course = getCourseWithString(courseID)
    return course


def isCourseMember(userID, courseID):
    user = getUser(userID)
    userIsCourseMember = False
    if len(user['courses']) > 0:
        for course in user['courses']:
            if course == courseID:
                userIsCourseMember = True
                break
    return userIsCourseMember


def isCourseOwner(userID, courseID):
    user = getUser(userID)
    userIsCourseOwner = False
    if user['isTutor'] and len(user['ownCourses']) > 0:
        for ownCourse in user['ownCourses']:
            if ownCourse == courseID:
                userIsCourseOwner = True
                break
    return userIsCourseOwner

# checking if user already exits by comparing mail
def userExists(mail):
    users = getAllUsers()
    user = next((x for x in users if x['mail'] == mail), None)
    return user is not None


def getUserWithMail(mail):
    users = getAllUsers()
    emptyUser = {}
    user = next((x for x in users if x['mail'] == mail), None)
    return user


def getUserWithID(id):
    users = getAllUsers()
    emptyUser = {}
    user = next((x for x in users if x['id'] == id), None)
    return user


def getUserFromSession():
    if 'mail' in session:
        return getUserWithMail(session['mail'])
    else:
        return None


# checking if user is logged in
def isLoggedIn():
    return 'mail' in session
    

def insertProgressAnswer(userMail, foreignKey, answerValue):
    answerAllreadyExist = False
    users = getAllUsersWrapperObject()
    for user in users['users']:
        if user['mail'] == userMail:
            for answer in user['progress']['answers']:
                if answer['foreignKey'] == foreignKey:
                    answerAllreadyExist = True
                    answer['value'] = answerValue
                    break
            
            if answerAllreadyExist == False:
                user['progress']['answers'].append({
                    'foreignKey': foreignKey,
                    'value': answerValue
                    })
            break
        
    updateDataBase('allUsers', users)
    

def insertProgressDownload(userMail, foreignKey):
    downloadAllreadyExist = False
    users = getAllUsersWrapperObject()
    for user in users['users']:
        if user['mail'] == userMail:
            for download in user['progress']['downloads']:
                if download['foreignKey'] == foreignKey:
                    downloadAllreadyExist = True
                    download['value'] = True
                    break
            
            if downloadAllreadyExist == False:
                user['progress']['downloads'].append({
                    'foreignKey': foreignKey,
                    'value': True
                    })
            break
        
    updateDataBase('allUsers', users)
    

def insertProgressDocument(userMail, foreignKey):
    documentAllreadyExist = False
    users = getAllUsersWrapperObject()
    for user in users['users']:
        if user['mail'] == userMail:
            for document in user['progress']['documents']:
                if document['foreignKey'] == foreignKey:
                    documentAllreadyExist = True
                    document['value'] = True
                    break
            
            if documentAllreadyExist == False:
                user['progress']['documents'].append({
                    'foreignKey': foreignKey,
                    'value': True
                    })
            break
        
    updateDataBase('allUsers', users)


#gibt den progress von recap-answers zurück
def getUserAnswer(mail, foreignKey):
    user = getUserByMail(mail)
    for answer in user['progress']['answers']:
        if answer['foreignKey'] == str(foreignKey):
            return answer['value']


#gibt den progress zur datei zurück, falls nicht vergeben false (durchsucht progress.downloads und progress.documents)
def getUserProgress(mail, foreignKey):
    user = getUserByMail(mail)

    for download in user['progress']['downloads']:
        if download['foreignKey'] == str(foreignKey):
            print('---> ' + download['foreignKey'] + ' == ' + str(foreignKey))
            return download['value']

    for document in user['progress']['documents']:
        if document['foreignKey'] == str(foreignKey):
            print('---> ' + document['foreignKey'] + ' == ' + str(foreignKey))
            return document['value']

    return False


@app.route('/changeTutorial/', methods=['GET'])
def editTutIndex():
    courseID = request.args.get('courseID')
    foundCourse = getCourseWithString(courseID)
    if isLoggedIn():
        userFromSession = getUserFromSession()
        for courseidSession in userFromSession['ownCourses']:
            if str(courseidSession) == courseID:
                if foundCourse is None:
                    return getIndex("Kurs nicht gefunden!")
                else:
                    return render_template('editTutorial.html', course=foundCourse)

    return getIndex("User nicht eingeloggt, oder nicht der Besitzer des Kurs")

@app.route('/deleteDownload/')
def deleteDownload():
    if isLoggedIn():
        courseID = request.args.get('courseID')
        downloadID = request.args.get('downloadID')
        user = getUserFromSession()
    
        if isCourseOwner(user['id'], ObjectId(courseID)):
            allCourses = getAllCoursesWrapperObject()
            foundCourse = None
            for course in allCourses['courses']:
                if str(course['id']) == courseID:
                    for download in course['courseDownloads']:
                        if str(download['fileID']) == downloadID:
                            course['courseDownloads'].remove(download)
                            print("Download aus Tutorial gelöscht")
                            break
                    foundCourse = course
                    break
            updateDataBase('allCourses', allCourses)
            return render_template('editTutorial.html', course = foundCourse)

    return getIndex("User nicht eingeloggt, oder nicht der Besitzer des Kurs")
    
@app.route('/deletePage/')
def deletePage():
    if isLoggedIn():
        courseID = request.args.get('courseID')
        docID = request.args.get('documentID')
        user = getUserFromSession()
    
        if isCourseOwner(user['id'], ObjectId(courseID)):
            allCourses = getAllCoursesWrapperObject()
            foundCourse = None
            for course in allCourses['courses']:
                if str(course['id']) == courseID:
                    for doc in course['categorys']['documents']:
                        if str(doc['id']) == docID:
                            course['categorys']['documents'].remove(doc)
                            print("Seite im Kurs gelöscht")
                            break
                    foundCourse = course
                    break
            updateDataBase('allCourses',allCourses)
            return render_template('editTutorial.html', course = foundCourse)

    return getIndex("User nicht eingeloggt, oder nicht der Besitzer des Kurs")


@app.route('/editTutorial/', methods=['POST'])
def editTutorial():
    courseID = request.args.get('courseID')
    course = getCourseWithString(courseID)
    if course is not None:
        if isLoggedIn() and isCourseOwner(getUserFromSession()['id'], course['id']):
            allCourses = getAllCoursesWrapperObject()

             # öffne Grid-Fs-Collection
            db = client.myTestBase
            fsCollection = gridfs.GridFS(db)

            courseBanner = request.files.getlist('courseBanner')
            courseName = request.form.get('courseName')
            courseDescription = request.form.get('courseDescription')
            pagesTitle = request.form.getlist('pageTitle')
            pagesStyle = request.form.getlist('pageStyle')
            pagesText = request.form.getlist('docText')
            countPages = request.form.get('countPages')
            fileDownloads = request.files.getlist('fileDownloads')
            fileDescription = request.form.get('fileDescription')

            if courseName is not course['name']:
                course['name'] = courseName

            if courseDescription is not course['description']:
                course['description'] = courseDescription

            if len(courseBanner) > 0:
                bannerID = ObjectId()
                fsCollection.delete(course['courseBannerID'])
                course['courseBannerID'] = bannerID
                fsCollection.put(
                    courseBanner[0], filename=courseBanner[0].filename, _id=bannerID)

            for x in range(0, int(countPages)):
                # wenn Dokument an der stelle x existiert, ersetze, sonst erstelle neues Dokument
                print("index ", x, " aktuelle Seitenanzahl ",len(course['categorys']['documents']), " neue Seitenanzahl ", countPages)
                if x < len(course['categorys']['documents']):
                    #ersetze Bilder oder Videos auf den Seiten des Tutorials
                    img = request.files.get('img'+str(x))
                    vid = request.files.get('vid'+str(x))
                    if pagesStyle[x] == '2' and img is not None:
                        print("neues img : ", img.filename)
                        #lösche alte Bilder und Videos
                        if course['categorys']['documents'][x]['content']['courseImgID'] is not None:
                            fsCollection.delete(course['categorys']['documents'][x]['content']['courseImgID'])
                            print("img gelöscht")
                            course['categorys']['documents'][x]['content']['courseImgID'] = None

                        if course['categorys']['documents'][x]['content']['courseVideoID'] is not None:
                            fsCollection.delete(course['categorys']['documents'][x]['content']['courseVideoID'])
                            print("vid gelöscht")
                            course['categorys']['documents'][x]['content']['courseVideoID'] = None

                        imgID = ObjectId()
                        course['categorys']['documents'][x]['content']['courseImgID'] = imgID
                        fsCollection.put(img, filename=img.filename, _id=imgID)
                        print("neues img hochgeladen")
                    elif pagesStyle[x] == '1' and vid is not None:
                        print("neues vid : ", vid.filename)
                        #lösche alte Bilder und Videos
                        if course['categorys']['documents'][x]['content']['courseImgID'] is not None:
                            fsCollection.delete(course['categorys']['documents'][x]['content']['courseImgID'])
                            print("img gelöscht")
                            course['categorys']['documents'][x]['content']['courseImgID'] = None

                        if course['categorys']['documents'][x]['content']['courseVideoID'] is not None:
                            fsCollection.delete(course['categorys']['documents'][x]['content']['courseVideoID'])
                            print("vid gelöscht")
                            course['categorys']['documents'][x]['content']['courseVideoID'] = None

                        videoID = ObjectId()
                        course['categorys']['documents'][x]['content']['courseVideoID'] = videoID
                        fsCollection.put(vid.read(), filename=vid.filename, _id=videoID)
                        print("neues vid hochgeladen")
                    #ersetze Seitentitel/Style/Texte
                    if pagesTitle[x] is not course['categorys']['documents'][x]['title']:
                        course['categorys']['documents'][x]['title'] = pagesTitle[x]
                        print("Seiten titel erneuert ", course['categorys']['documents'][x]['title'])
                    if pagesStyle[x] is not course['categorys']['documents'][x]['styleTyp']:
                        course['categorys']['documents'][x]['styleTyp'] = pagesStyle[x]
                        print("Seiten Style erneuert ", course['categorys']['documents'][x]['styleTyp'])
                    if pagesText[x] is not course['categorys']['documents'][x]['content']['p'][0]:
                        course['categorys']['documents'][x]['content']['p'][0] = pagesText[x]
                        print("Text erneuert ", course['categorys']['documents'][x]['content']['p'][0])
        
                else:
                    #wenn seite noch nicht existiert erstelle neues Dokument
                    imgID = ObjectId()
                    videoID = ObjectId()

                    # Neues Dokument
                    newDoc = newDocument()
                    if len(pagesTitle) > x:
                        newDoc['title'] = pagesTitle[x]
                        newDoc['styleTyp'] = pagesStyle[x]
                    if len(pagesText) > x:
                        newDoc['content']['p'].append(pagesText[x])

                    if pagesStyle[x] == '2':
                        img = request.files.get('img'+str(x))
                        if img is not None:
                            newDoc['content']['courseImgID'] = imgID
                            fsCollection.put(img, filename=img.filename, _id=imgID)

                    if pagesStyle[x] == '1':
                        vid = request.files.get('vid'+str(x))
                        if vid is not None:
                            newDoc['content']['courseVideoID'] = videoID
                            fsCollection.put(vid.read(), filename=vid.filename, _id=videoID)

                    course['categorys']['documents'].append(newDoc)
                    print("Neue Seite zum Tutorial hinzugefügt")

            # hänge fileDownloads ins Grid-fs und die ID dazu in das Tutorial unter courseDownloads an.
            course['courseDownloadDescription'] = fileDescription
            for x in range(0, len(fileDownloads)):
                fileID = ObjectId()
                fsCollection.put(
                    fileDownloads[x], filename=fileDownloads[x].filename, _id=fileID)
                courseDownload = newCourseDownload()
                courseDownload['fileID'] = fileID
                courseDownload['fileName'] = fileDownloads[x].filename
                course['courseDownloads'].append(courseDownload)
            
            #update DB
            for j in range(0, len(allCourses['courses'])):
                if allCourses['courses'][j]['id'] == course['id']:
                    allCourses['courses'][j] = course
                    break
            updateDataBase('allCourses', allCourses)
            # öffne bearbeitetes Tutorium
            return renderTutorialPrePage(course)
        else:
            return getIndex("Sie sind nicht eingeloggt, oder nicht der Besitzer des Tutorials")
    else:
        return getIndex("Kurs zum bearbeiten nicht gefunden.")

@app.route('/', methods=['GET'])
def getIndex(info = None):
    courses = getAllCourses()
    requiredCourses = getIndexTutorials(courses)
    for course in requiredCourses['Satz0']:
        if course['id'] != None:
            course['courseImg'] = course['courseBannerID']

    for course in requiredCourses['Satz1']:
        if course['id'] != None:
            course['courseImg'] = course['courseBannerID']

    # langingPage.html erbt von unloggedLayout oder loggedLayout,
    # userLoged entscheidet, von welchem der Templates geerbt werden soll
    if isLoggedIn():
        if info is not None:
            return render_template('landingPage.html', userLoged=True, courses=requiredCourses, username=getUserFromSession()['nickname'], info = info)
        else:
            return render_template('landingPage.html', userLoged=True, courses=requiredCourses, username=getUserFromSession()['nickname'])
    else:
        if info is not None:
            return render_template('landingPage.html', userLoged=False, courses=requiredCourses, info = info)
        else:
            return render_template('landingPage.html', userLoged=False, courses=requiredCourses)


@app.route('/addUserCourse/')
def addCourse():
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)

    if course is not None and isLoggedIn():
        userFromSession = getUserFromSession()
        allUser = getAllUsersWrapperObject()
        for user in allUser['users']:
            if user['id'] == userFromSession['id']:
                user['courses'].append(course['id'])
                break
        updateDataBase('allUsers', allUser)

    return renderTutorialPrePage(course)


@app.route('/delUserCourse/')
def delCourse():
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)

    if course is not None and isLoggedIn():
        userFromSession = getUserFromSession()
        allUser = getAllUsersWrapperObject()
        for user in allUser['users']:
            if user['id'] == userFromSession['id']:
                for userCourse in user['courses']:
                    if userCourse == course['id']:
                        user['courses'].remove(userCourse)
                        break
                break
        updateDataBase('allUsers', allUser)

    return renderTutorialPrePage(course)


@app.route('/searchTutorial/', methods=['POST'])
def searchTutorial():
    searchText = request.form.get('search-bar')
    searchText = searchText.lower()
    foundCourses = []
    allCourses = getAllCourses()
    for course in allCourses:
        courseName = course['name'].lower()
        courseDesc = ''
        if course['description'] is not None:
            courseDesc = course['description'].lower()
        if searchText in courseName or searchText in courseDesc:
            foundCourses.append(course)
    if isLoggedIn():
        return render_template('searchTutorial.html', courses = foundCourses, userLoged=True, username=getUserFromSession()['nickname'])
    else:
        return render_template('searchTutorial.html', userLoged=False)
    

@app.route('/uploadTutorial/', methods=['POST', 'GET'])
def uploadTutorial():
    if not isLoggedIn():
        print()
        return getIndex("Nicht eingeloggt")

    userFromSession = getUserWithMail(session['mail'])
    if request.method == 'POST' and userFromSession['isTutor']:

        courseBanner = request.files.getlist('courseBanner')
        courseName = request.form.get('courseName')
        courseDescription = request.form.get('courseDescription')

        pagesTitle = request.form.getlist('pageTitle')
        pagesStyle = request.form.getlist('pageStyle')
        # pagesVideo = request.files.getlist('videoFile')
        pagesText = request.form.getlist('docText')
        pagesText2 = request.form.getlist('docText2')
        # pagesImg = request.files.getlist('courseImg')
        countPages = request.form.get('countPages')
        fileDownloads = request.files.getlist('fileDownloads')
        fileDescription = request.form.get('fileDescription')

        newTut = newEmptyCourse()
        if courseName:
            newTut['name'] = courseName
        else:
            return render_template('upload.html', info='Geben Sie mindestens einen Namen für das Tutorial an.')
        if courseDescription:
            newTut['description'] = courseDescription

        # öffne Grid-Fs-Collection
        db = client.myTestBase
        fsCollection = gridfs.GridFS(db)

        # für Kurs-banner
        bannerID = ObjectId()
        if len(courseBanner) > 0:
            newTut['courseBannerID'] = bannerID
            fsCollection.put(
                courseBanner[0], filename=courseBanner[0].filename, _id=bannerID)

        newTut['courseDownloadDescription'] = fileDescription
     # für jede Seite im erstellten Kurs:

        for x in range(0, int(countPages)):
            # für Kurs Img/video
            imgID = ObjectId()
            videoID = ObjectId()

            # Neues Dokument
            newDoc = newDocument()
            if len(pagesTitle) > x:
                newDoc['title'] = pagesTitle[x]
            newDoc['styleTyp'] = pagesStyle[x]
            if len(pagesText) > x:
                newDoc['content']['p'].append(pagesText[x])
            if len(pagesText2) > x:
                newDoc['content']['p'].append(pagesText2[x])

            if pagesStyle[x] == '2':
                img = request.files.get('img'+str(x))
                if img is not None:
                    newDoc['content']['courseImgID'] = imgID
                    fsCollection.put(img, filename=img.filename, _id=imgID)

            if pagesStyle[x] == '1':
                vid = request.files.get('vid'+str(x))
                if vid is not None:
                    newDoc['content']['courseVideoID'] = videoID
                    fsCollection.put(
                        vid.read(), filename=vid.filename, _id=videoID)

            newTut['categorys']['documents'].append(newDoc)

       # hänge fileDownloads ins Grid-fs und die ID dazu in das Tutorial unter courseDownloads an.
        for x in range(0, len(fileDownloads)):
            fileID = ObjectId()
            fsCollection.put(
                fileDownloads[x], filename=fileDownloads[x].filename, _id=fileID)
            courseDownload = newCourseDownload()
            courseDownload['fileID'] = fileID
            courseDownload['fileName'] = fileDownloads[x].filename
            newTut['courseDownloads'].append(courseDownload)

       # hänge KursID an die OwnCourses vom Tutor aus der Session
        allUser = getAllUsersWrapperObject()
        for user in allUser['users']:
            if user['id'] == userFromSession['id']:
                user['ownCourses'].append(newTut['id'])
                break
        updateDataBase('allUsers', allUser)

        # hänge neuen Kurs an alle Kurse ran
        allCourses = getAllCoursesWrapperObject()
        allCourses['courses'].append(newTut)
        # update alle Kurse in DB
        updateDataBase('allCourses', allCourses)
        # öffne erstelltes Tutorium
        return renderTutorialTemplate(newTut, 0, newTut['categorys']['documents'][0]['content']['courseImgID'],
                                      newTut['categorys']['documents'][0]['content']['courseVideoID'])
    if request.method == 'GET' and userFromSession != None:
        # Wenn Seite erst aufgerufen werden soll
        if userFromSession['isTutor']:
            return render_template('upload.html', username=userFromSession['nickname'])
        else:
            return getIndex("User ist kein Tutor")
    else:
        return getIndex("Unbekannter Fehler")


@app.route('/recap', methods=['POST', 'GET'])
def recap():
    if request.method == 'POST':
        #method is post: save recap
        courseID = request.form.get('courseID')
        recap = newRecap()

        #get recap from post request
        questionCounter = 1
        while(request.form.get('questionText_' + str(questionCounter))):
            question = newQuestion()
            question['questionText'] = request.form.get('questionText_' + str(questionCounter))
            answerCounter = 1
            while(request.form.get('question_' + str(questionCounter) + '_answer_' + str(answerCounter))):
                answer = newAnswer()
                answer['answerText'] = request.form.get('question_' + str(questionCounter) + '_answer_' + str(answerCounter))
                if request.form.get('question_' + str(questionCounter) + '_isCorrectAnswer_' + str(answerCounter)):
                    answer['answerIsCorrect'] = True
                else:
                    answer['answerIsCorrect'] = False
                question['answers'].append(answer)
                answerCounter += 1
            
            recap['questions'].append(question)
            questionCounter += 1

        #del all given answers from users
        users = getAllUsersWrapperObject()
        users = getAllUsersWrapperObject()
        for user in users['users']:
            for userAnswer in reversed(user['progress']['answers']):
                for courseQuestion in getCourseWithString(courseID)['recap']['questions']:
                    for courseAnswer in courseQuestion['answers']:
                        if userAnswer['foreignKey'] == str(courseAnswer['id']):
                            user['progress']['answers'].remove(userAnswer)
        updateDataBase('allUsers', users)
        
        #save recap in mongo
        courses = getAllCoursesWrapperObject()
        for course in courses['courses']:
            if str(course['id']) == courseID:
                course['recap'] = recap
                break

        updateDataBase('allCourses', courses)

        course = getCourseWithString(courseID)
        return renderFirstPage(course)
    else:
        #method is get: show recap
        courseID = request.args.get('courseID')
        course = getCourseIfExists(courseID)

        if isCourseOwner(getUserByMail(session['mail'])['id'], course['id']):
            #show recap for owner
            return render_template('tutorialRecapEdit.html',
                course = course,
                userLogged=isLoggedIn(),
                userIsCourseMember = isCourseMember(getUserFromSession()['id'], course['id']),
                userIsCourseOwner = isCourseOwner(getUserFromSession()['id'], course['id']))
        else:
            #show recap for user

            #prepare courses dictonary - insert user progress
            for question in course['recap']['questions']:
                for answer in question['answers']:
                    userAnswer = getUserAnswer(session['mail'], answer['id'])
                    answer['userWasCorrect'] = answer['answerIsCorrect'] == userAnswer
                    answer['userChoose'] = userAnswer

            return render_template('tutorialRecap.html',
                course = course,
                userLogged=isLoggedIn(),
                userIsCourseMember = isCourseMember(getUserFromSession()['id'], course['id']),
                userIsCourseOwner = isCourseOwner(getUserFromSession()['id'], course['id']))
            

@app.route('/recapAnswer', methods=['POST'])
def recapAnswer():
    courseID = request.args.get('courseID')
    questionCounter = 1
    while(request.form.get('question_' + str(questionCounter))):
        
        answerCounter = 1
        while(request.form.get('question_' + str(questionCounter) + '_answer_' + str(answerCounter) + '_id')):
            answerID = request.form.get('question_' + str(questionCounter) + '_answer_' + str(answerCounter) + '_id')
            isChecked = False
            if request.form.get('question_' + str(questionCounter) + '_answer_' + str(answerCounter) + '_isCorrect'):
                isChecked = True
                
            insertProgressAnswer(session['mail'], answerID, isChecked)

            answerCounter += 1
        questionCounter += 1

    course = getCourseWithString(courseID)
    return renderFirstPage(course)

def renderTutorialPrePage(course):
    # sende Vorseite zum Tutorial 
    user = getUserFromSession()
    if user is not None:
        if isCourseOwner(user['id'], course['id']):
            return render_template('tutorialDetailsForTutor.html', course=course, username=user['nickname'])
        else:
            isMember = False
            for courseid in user['courses']:
                if courseid == course['id']:
                    isMember = True
                    break
            return render_template('tutorialDetailsForUser.html', course=course, username=user['nickname'], isMember=isMember)
    else:
        return render_template('tutorialDetailsForGuest.html', course=course)

@app.route('/TutorialOverview/')
def getTutorialOverview():
    if isLoggedIn():
        user = getUserFromSession()
        isTutor = user['isTutor']

        courses = getAllCourses()
        
        memberCourses = []
        ownCourses = []

        #für alle KursId, in denen der User eingetragen ist,
        for courseID in user['courses']:
            #durchsuche alle Kurse und hänge Kurs an memberCourses
            for course in courses:
                if courseID == course['id']:
                    memberCourses.append(course)
                    break

        #für alle KursId, in eigenen Kursen vom User,
        for ownCourseID in user['ownCourses']:
            #durchsuche alle Kurse und hänge Kurs an ownCourses
            for course in courses:
                if ownCourseID == course['id']:
                    ownCourses.append(course)
                    break
        print(memberCourses)
        return render_template('tutorialOverview.html', memberCourses = memberCourses, ownCourses = ownCourses, userisTutor = isTutor)
    else:
        return getIndex("Nutzer nicht eingeloggt")


@app.route('/TutorialChat/', methods=['GET'])
def getCourseChat():
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)
    if course is not None:
        if isLoggedIn():
            return render_template('tutorialChat.html',
                username=getUserFromSession()['nickname'],
                userLogged=True,
                course=course,
                userIsCourseMember = isCourseMember(getUserFromSession()['id'], course['id']),
                userIsCourseOwner = isCourseOwner(getUserFromSession()['id'], course['id']))
        else:
            return getIndex("Nicht eingelogget!")
    else:
        return getIndex("Kurs nicht gefunden")


@app.route('/TutorialProgress/', methods=['GET'])
def getTutorialProgress():
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)

    #prepare courses dictonary - insert user progress recap
    print(course['recap'])
    if course['recap'] is not None:
        for question in course['recap']['questions']:
            for answer in question['answers']:
                userAnswer = getUserAnswer(session['mail'], answer['id'])
                answer['userWasCorrect'] = answer['answerIsCorrect'] == userAnswer
                answer['userChoose'] = userAnswer

    #prepare courses dictonary - insert user progress document
    for document in course['categorys']['documents']:
        document['userProgress'] = getUserProgress(session['mail'], document['id'])
        print('document seen: ' + str(getUserProgress(session['mail'], document['id'])))

    #prepare courses dictonary - insert user progress download
    for download in course['courseDownloads']:
        download['userProgress'] = getUserProgress(session['mail'], download['fileID'])
        print('download downloaded: ' + str(getUserProgress(session['mail'], download['fileID'])))

    return render_template('tutorialProgress.html',
        username=getUserFromSession()['nickname'],
        userLogged=True,
        course=course,
        userIsCourseMember = isCourseMember(getUserFromSession()['id'], course['id']),
        userIsCourseOwner = isCourseOwner(getUserFromSession()['id'], course['id']))


@app.route('/TutorialDownloads/', methods=['GET'])
def getCourseDownloads():
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)
    if course is not None:
        if isLoggedIn():
            return render_template('tutorialDownloads.html',
                username=getUserFromSession()['nickname'],
                userLogged=True,
                course=course,
                userIsCourseMember = isCourseMember(getUserFromSession()['id'], course['id']),
                userIsCourseOwner = isCourseOwner(getUserFromSession()['id'], course['id']))
        else:
            return render_template('tutorialDownloads.html',
                userLogged=False,
                course=course)
    else:
        return getIndex("Kurs nicht gefunden")
      

@app.route('/Tutorial/')
def getTutorialWithDocumentID():
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)
    documentID = request.args.get('documentID')

    if documentID is not None:
        #insert progress
        if isLoggedIn():
            insertProgressDocument(session['mail'], documentID)

        documentIndex = getDocumentIndex(documentID, course)
        documentImgID = course['categorys']['documents'][documentIndex]['content']['courseImgID']
        documentVideoID = course['categorys']['documents'][documentIndex]['content']['courseVideoID']
        return renderTutorialTemplate(course, documentIndex, documentImgID, documentVideoID)
    else:
        return renderTutorialPrePage(course)


def renderFirstPage(course):
        docImg = course['categorys']['documents'][0]['content']['courseImgID']
        docVid = course['categorys']['documents'][0]['content']['courseVideoID']
        return renderTutorialTemplate(course, 0, docImg, docVid)


@app.route('/editProfile', methods=['POST', 'GET'])
def editProfile():
    if request.method == 'POST' and isLoggedIn():
        mail = request.form.get('mail')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        isTutor = request.form.get('isTutor')
        if len(mail) > 0 and len(firstName) > 0 and len(lastName) > 0 :
            allUsers = getAllUsersWrapperObject()
            user = getUserFromSession()
            if mail is not user['mail']:
                user['mail'] = mail
                session['mail'] = mail
            if firstName is not user['first_name']:
                user['first_name'] = firstName
            if lastName is not user['last_name']:
                user['last_name'] = lastName
            if nickname is not user['nickname']:
                user['nickname'] = nickname
                session['nickname'] = nickname
            if password is not '' and password == password2:
                user['passphrase'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if isTutor is not user['isTutor']:
                user['isTutor'] = isTutor
            # or , item in enumerate(alist)
            for idx,userFromAllUsers in enumerate(allUsers['users']):
                if user['id'] == userFromAllUsers['id']:
                    allUsers['users'][idx] = user
                    break
            updateDataBase('allUsers', allUsers)
            return render_template('editProfile.html', user = user, info = "applied changes")

    elif request.method == 'GET' and isLoggedIn():
        user = getUserFromSession()
        return render_template('editProfile.html', user = user)
    else:
        return getIndex("User nicht eingeloggt")


# show register form or save register informations in mongo
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        mail = request.form.get('mail')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        isTutor = request.form.get('isTutor')

        # checking if inputs are valide
        if len(mail) > 0 and len(firstName) > 0 and len(lastName) > 0 and len(password) > 0 and password == password2:

            # check if the user already exists
            if userExists(mail) == False:
                # get all users
                allUsers = getAllUsersWrapperObject()

                # generate salted hash
                passphrase = bcrypt.hashpw(
                    password.encode('utf-8'), bcrypt.gensalt())

                # create new user
                singleExampleUser = newEmptyUser()
                singleExampleUser['mail'] = mail
                singleExampleUser['first_name'] = firstName
                singleExampleUser['last_name'] = lastName
                singleExampleUser['nickname'] = nickname
                singleExampleUser['passphrase'] = passphrase
                if isTutor is None:
                    singleExampleUser['isTutor'] = False
                else:
                    singleExampleUser['isTutor'] = True

                # append user
                allUsers['users'].append(singleExampleUser)

                # update alle Kurse in DB
                updateDataBase('allUsers', allUsers)

                # logging in user
                session['mail'] = mail
                session['nickname'] = nickname

                return getIndex("User added")
            else:
                return getIndex("User already exists")
        else:
            return getIndex("user data not correct")
    else:
        user = getUserFromSession()
        if user is not None:
            return getIndex("Already logged")
        else:
            return render_template('register.html', userLoged = False)

        


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        mail = request.form.get('mail')
        password = request.form.get('password')

        user = getUserByMail(mail)

        if user:
            if bcrypt.hashpw(password.encode('utf-8'), user['passphrase']) == user['passphrase']:
                session['mail'] = mail
                session['nickname'] = user['nickname']
                return getIndex()

        return getIndex("Invalid username or password")
    else:
        return getIndex()


@app.route('/logout')
def logout():
    session.clear()
    return getIndex()


@app.route('/chat')
def testchat():
    return render_template('ws-client.html')

# --------Get BootStrap-Content-Routen-------
@app.route('/assets/bootstrap/css/<filename>')
def send_bootStrapCss(filename):
    return send_from_directory("templates/assets/bootstrap/css", filename)


@app.route('/assets/bootstrap/js/<filename>')
def send_bootStrapJs(filename):
    return send_from_directory("templates/assets/bootstrap/js", filename)


@app.route('/assets/css/<filename>')
def send_css(filename):
    return send_from_directory("templates/assets/css", filename)


@app.route('/assets/fonts/<filename>')
def send_fonts(filename):
    return send_from_directory("templates/assets/fonts", filename)


@app.route('/assets/img/<filename>')
def send_image(filename):
    return send_from_directory("templates/assets/img", filename)


@app.route('/assets/js/<filename>')
def send_js(filename):
    return send_from_directory("templates/assets/js", filename)
# ------------------------------------------------
@app.route('/websocketChat/<filename>')
def send_WsChat(filename):
    return send_from_directory("websocketChat", filename)


@app.route('/video/<videoid>')
def getVideo(videoid):
    if videoid != 'None':
        print("VideoID : ", videoid)
        # öffne Grid-Fs-Collection
        db = client.myTestBase
        fsCollection = gridfs.GridFS(db)
        videoFile = fsCollection.get_last_version(_id=ObjectId(videoid))
        filename = videoFile.filename
        print("DateiName: ", filename)

        response = make_response(videoFile.read())
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            filename)
    else:
        return ''
    return response


@app.route('/img/<imgid>')
def getImg(imgid):
    if imgid != 'None':
        # öffne Grid-Fs-Collection
        db = client.myTestBase
        fsCollection = gridfs.GridFS(db)
        imgFile = fsCollection.get_last_version(_id=ObjectId(imgid))
        filename = imgFile.filename
        print("DateiName: ", filename)

        response = make_response(imgFile.read())
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            filename)
    else:
        return ''
    return response


@app.route('/download/<fileid>')
def getDownloadFile(fileid):
    if fileid != 'None':
        #insert progress
        if isLoggedIn():
            insertProgressDownload(session['mail'], fileid)

        db = client.myTestBase
        fsCollection = gridfs.GridFS(db)
        downloadFile = fsCollection.get_last_version(_id=ObjectId(fileid))
        filename = downloadFile.filename
        print("DateiName: ", filename)
        
        response = make_response(downloadFile.read())
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            filename)
    else:
        print("id leer")
        return ''
    return response



# startpunkt des py-programms
if __name__ == "__main__":
    #deleteCollection()

    #initDB()
    # fillDB()

    app.secret_key = 'oiwfhwinehi'  # add rnd chars here
    app.run(debug=True, host='0.0.0.0')
