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
        'ownCourses': []
    }


def newEmptyCourse():
    return {
        'id': ObjectId(),
        'name': None,
        'description': None,
        'courseBannerID': None,
        'courseDownloads': [],
        'categorys': {
            'documents': [],
            'quiz': []},
    }


def newCourseDownload():
    return {
        'fileID': None,
        'fileName': None,
        'description': None
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


def newQuiz():
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
    #newTutorial['id'] = '1234567890qwertzuio2'
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
    #newTutorial2['id'] = '1234567890qwertzuio'
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
    foundcourse = {}
    for course in allCourses:
        if course['id'] == courseID:
            foundcourse = course
            break

    return foundcourse


def getCourseWithString(courseID):
    allCourses = getAllCourses()
    foundcourse = {}
    for course in allCourses:
        print("DB ", course['id'], " courseID ", courseID)
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
        print("Template 1 ausgeführt")
        if isLoggedIn():
            templateToRender = render_template('tutorialStyle1.html', username=getUserFromSession()['nickname'], userLogged=True, course=course, documentIndex=documentIndex,
                                               documentImgID=documentImgID, documentVideoID=documentVideoID)
        else:
            templateToRender = render_template('tutorialStyle1.html', userLogged=False, course=course, documentIndex=documentIndex,
                                               documentImgID=documentImgID, documentVideoID=documentVideoID)
    else:
        print("Template 2 ausgeführt")
        if isLoggedIn():
            templateToRender = render_template('tutorialStyle2.html', username=getUserFromSession()['nickname'], userLogged=True, course=course, documentIndex=documentIndex,
                                               documentImgID=documentImgID)
        else:
            templateToRender = render_template('tutorialStyle2.html', userLogged=False, course=course, documentIndex=documentIndex,
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
    else:
        print("Tutorial nicht vorhanden")
    return course


def isCourseOwner(userID, courseID):
    user = getUser(userID)
    userIsCourseOwner = False
    if user['isTutor'] and len(user['ownCourses']) > 0:
        for ownCourses in user['ownCourses']:
            print(ownCourses, " and ", courseID)
            if ownCourses == courseID:
                userIsCourseOwner = True
                break
    return userIsCourseOwner

# checking if user already exits by comparing mail


def userExists(mail):
    users = getAllUsers()
    user = next((x for x in users if x['mail'] == mail), None)
    return user is not None


def getuserWithMail(mail):
    users = getAllUsers()
    emptyUser = {}
    user = next((x for x in users if x['mail'] == mail), None)
    return user


def getUserFromSession():
    if 'mail' in session:
        return getuserWithMail(session['mail'])
    else:
        return None

# checking if user is logged in


def isLoggedIn():
    return 'mail' in session


@app.route('/changeTutorial/', methods=['GET'])
def editTutIndex():
    courseID = request.args.get('courseID')
    emptyCourse = {}
    foundCourse = getCourseWithString(courseID)
    if isLoggedIn():
        userFromSession = getUserFromSession()
        for courseidSession in userFromSession['ownCourses']:
            if str(courseidSession) == courseID:
                if foundCourse == emptyCourse:
                    print("Kurs nicht gefunden!")
                    return getIndex()
                else:
                    return render_template('editTutorial.html', course=foundCourse)

    print("User nicht eingeloggt, oder nicht der Besitzer des Kurs")
    return getIndex()

# Wenn Tutorial schon existiert


@app.route('/editTutorial', methods=['POST'])
def editTutorial():
    #userID = request.args.get('cookieID')
    courseID = request.args.get('courseID')
    # if isCourseOwner(userID, courseID)
    courseIndex = getCourseIndex(courseID)
    allCourses = getAllCoursesWrapperObject()
    # bearbeite KursInformationen

    # Wenn Feld leer, überschreibe nicht!!!!!!!!111

    #allCourses['courses'][courseIndex]['courseImgID'] = imgID


@app.route('/', methods=['GET'])
def getIndex():
    courses = getAllCourses()
    requiredCourses = getIndexTutorials(courses)
    for course in requiredCourses['Satz0']:
        if course['id'] != None:
            course['courseImg'] = course['courseBannerID']

    for course in requiredCourses['Satz1']:
        if course['id'] != None:
            course['courseImg'] = course['courseBannerID']

    # langingPage.html erbt von unloggedLayout oder loggedLayout,
    # userLoged entscheidet, von welchem der Templates geerbt werden soll, nice oder? :D
    if isLoggedIn():
        return render_template('landingPage.html', userLoged=True, courses=requiredCourses, username=getUserFromSession()['nickname'])
    else:
        return render_template('landingPage.html', userLoged=False, courses=requiredCourses)
    # return render_template('indexKristof.html')


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

    # if string1.lower() == string2.lower():
    # print "The strings are the same (case insensitive)"
    

@app.route('/uploadTutorial/', methods=['POST', 'GET'])
def uploadTutorial():
    if not isLoggedIn():
        print("Nicht eingeloggt")
        return getIndex()

    userFromSession = getuserWithMail(session['mail'])
    if request.method == 'POST' and userFromSession['isTutor']:

        courseBanner = request.files.getlist('courseBanner')
        courseName = request.form.get('courseName')
        courseDescription = request.form.get('courseDescription')

        pagesTitle = request.form.getlist('pageTitle')
        pagesStyle = request.form.getlist('pageStyle')
        #pagesVideo = request.files.getlist('videoFile')
        pagesText = request.form.getlist('docText')
        pagesText2 = request.form.getlist('docText2')
        #pagesImg = request.files.getlist('courseImg')
        countPages = request.form.get('countPages')
        fileDownloads = request.files.getlist('fileDownloads')
        fileDescription = request.form.getlist('fileDescription')

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

            elif pagesStyle[x] == '1':
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
            courseDownload['description'] = fileDescription[x]
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
    elif request.method == 'GET' and userFromSession != None:
        #Wenn Seite erst aufgerufen werden soll
        if userFromSession['isTutor']:
            return render_template('upload.html', username=userFromSession['nickname'])
        else:
            print("User ist kein Tutor")
            return getIndex()
    else:
        return getIndex()


# Wahrscheinlich nicht mehr notwendig, /Tutorial/ behandelt alles hieraus
# @app.route('/Tutorial', methods=['GET'])
# def getTutorialWithoutDocumentID():
#     courseID = request.args.get('courseID')
#     course = getCourseIfExists(courseID)

#     # documentIndex immer 0, wenn Tutorial ohne Dokument geöffnet wird
#     documentIndex = 0

#     documentImgID = course['categorys']['documents'][documentIndex]['content']['courseImgID']
#     documentVideoID = course['categorys']['documents'][documentIndex]['content']['courseVideoID']

#     return renderTutorialTemplate(course, documentIndex, documentImgID, documentVideoID)

# Um auf die anderen Seiten des Tutorials zu kommen
def renderTutorialPrePage(course):
    # In diesem Fall, sende Vorseite zum Tutorial (zum Kurs, teilnehmen, teilnahme beenden, tut bearbeiten)
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


@app.route('/TutorialDownloads/', methods=['GET'])
def getCourseDownloads():
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)

    return render_template('tutorialDownloads.html', course=course)


@app.route('/Tutorial/')
def getTutorialWithDocumentID():
    # cookieID =  #readCookie()
    courseID = request.args.get('courseID')
    course = getCourseIfExists(courseID)

    documentID = request.args.get('documentID')
    if documentID is not None:
        documentIndex = getDocumentIndex(documentID, course)
        documentImgID = course['categorys']['documents'][documentIndex]['content']['courseImgID']
        documentVideoID = course['categorys']['documents'][documentIndex]['content']['courseVideoID']
        return renderTutorialTemplate(course, documentIndex, documentImgID, documentVideoID)
    else:
        return renderTutorialPrePage(course)
        # show register form or save register informations in mongo

@app.route('/websocketChat/<filename>') 
def send_WsChat(filename): 
    return send_from_directory("websocketChat", filename) 

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

                #logging in user
                session['mail'] = mail

                return 'user added'
            else:
                return 'user already exists'
        else:
            return 'user data not correct'
    else:
        return render_template('register.html')


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
                print("logged in")
                return getIndex()

        return 'Invalid username/password combination'
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
# geht auch mit file, statt videos und imgs getrennt zu behandeln, später ändern!


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
    # deleteCollection()

    # initDB()
    # fillDB()

    app.secret_key = 'oiwfhwinehi'  # add rnd chars here
    app.run(debug=True, host='0.0.0.0')
