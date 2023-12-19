# HOLLY.APP
#### Video Demo: https://youtu.be/FFzkCN5albY?si=PHIYStC3Q0lsmHFB
#### Description:
hello, my name is Pedro vieira, I speak from Rio de Janeiro, Brazil, and this is my 
final project of CS50’s Web Programming with Python and JavaScript.
my project is called Holly.app,
it takes that name because my project aims to facilitate the activities of religious entities in 'Rio de janeiro', 
such as churches, synagogues, mosques, etc. It focuses mainly on the findability of these entities and their 
communication with the faithful.
all project was made in Django(python) for the back-end, and HTML5/CSS3/JS without any framework, only the CSS bootstrap, for front-end and SQLite for manage the database.

## SUMMARY
My program helps religious entities communicate with their members;
and helps people find the cells of their religions in the regions chosen by them.

For normal users, the home screen will be a form with the religion and a select list with the cities in the state of 'Rio de Janeiro' and their subregions, if any.
And based on this, the application will search the database for entities of that specific religion and region,
clicking on one of these entities. the user will be redirected to its page, 
there their can become a member and see its summary and communications.
Furthermore, there is a page where the user can check all the announcements from the entities they are members of;
and there is also a page with all entities registered on the platform.

For registration entities, they can make announcements about their activities and edit them if they wish. 
in addition to being able to edit their own data, such as location, religion and summary.
And entities can interact with each other like an average user.

## DISTINCTIVENESS AND  COMPLEXITY 
My projects satisfy the distinction and complexity due to the fact that their 
'CRUD' functions to create, change and read are more complex than previous projects.
for example:

to create a user, first there is the distinction between a normal user
and an entity user, if it is an entity, there are different capabilities and, at the time
of registration, there are different fields that appear responsively, using JS, and some fields
consume an external API which were also complex; 

To edit user data, js is used to open an editing menu responsively, 
some fields consume an external API and text fields already appear filled with previous
texts. Additionally, there is a button to cancel this edit, which will make the edit
menu disappear responsively;

to read the data, the complexity is mainly in the initial search screen, where using js,
2 or 3 place selection bars and a religion selection bar will appear, and with this data,
the system will return all the entities that suit the filter

In addition to these functions, the consumption of external APIs was quite complex.
To get the cities and neighborhoods of the state of Rio de Janeiro (RJ),
I used a government API that returns the cities of RJ, and when this city is selected
by the user, another select appears responsively below this one using js, and This other
select searches all neighborhoods of the city. However, there are neighborhoods that are very large
and therefore have sub-regions within them. So, if this sub-region has sub-regions,
using the API again, another select will appear with these sub-regions. For the "form" in html,
if there are no sub-regions, only the city and sub-region will be taken into account;
but if there is a sub-sub-region, only the city and the sub-sub-region will be taken into account,
this is used both for the features of searching for entities, creating
entities and editing entities

on responsiveness is also worth highlighting. Using just JS, there were the animations
for the buttons for making an announcement and editing data, in which the menus collapse
and appear; and the animations of the locations selects appearing one after the other

Another considerable detail is the creation of pagination, 
advertisements and entities templates, enabling their reuse

## Important files and folders

### -holly.static.imgs
folders that contain the images used in the project, in this case a single image of 
Rio de Janeiro, the one used on the site's main search page.
### -holly.static.holly.index.js
This file is where the JavaScript codes are located. 
its main methods are:

#### - *carregarLugares* ('loadPlaces' in english)
this function loads a select that has the id "localSelect" with the cities of Rio de Janeiro

    const carregarLugares = () =>{
        let select1 = document.getElementById("localSelect");
        fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/33/municipios`)
        .then(response => response.json())
        .then(citys => citys.forEach(city => {
            let citynew = document.createElement("option");
            citynew.value = city.id;
            citynew.innerHTML = city.nome;
            citynew.dataset.nome = city.nome;
            select1.appendChild(citynew);
            select1.selectedIndex = -1;
        }));
    };
#### - *changerRegisterEntity*
This function changes the registration menu depending on whether the user is 
normal or a religious entity

    const changerRegisterEntity = (node) =>{
        let registerEntity = document.getElementById("registerEntity");
        if(node.value == "True"){
            registerEntity.hidden = false;
        }
        else if(node.value == "False"){
            registerEntity.hidden = true;
        }
    };

#### - *edit*
function that makes the edit menu appear and it possible to edit announcements from entities
there are other functions that help it, such as the *showAnnounce* and
*cancelAnnounce* functions, which will act on the appearance of the menu and its cancellation.

    const edit = (userId, announeId) => {
        announeId = parseInt(announeId);
        userId = parseInt(userId);
        fetch(`/edit/${announeId}`)
            .then(response => response.json())
            .then(announce => {
                if (announce.user == userId) {
                    document.getElementById(announce.id).innerHTML = `
                    <form>
                    <textarea name="text" rows="4" style="width: 100%" id ="edit-text">${announce.text}</textarea>
                    <br>
                    <input type="submit" class="btn btn, butao" onclick="announceEdit(event, ${announeId}, ${userId})" value="Edit">
                    </form>`;
                } else {
                    document.getElementById(announce.id).innerHTML = "ERROR";
                }
            });
    };

#### - *loadneighbourhood & loadSubdistritos & changeFake*
loadneighbourhood: makes the neighborhoods select appear and loads a select with the neighborhoods, based on the results of the
cities select, using an API 

loadSubdistritos: makes the subregions select appear and load the subregions if they exist, using an API 

changeFake: manages which data will be sent with "neighborhood",
the neighborhood or subregions if they exist

    const loadneighbourhood = () => {
        let idMunicipio = document.getElementById("localSelect").value;
        let neighbourhoodSelect = document.getElementById("neighbourhoodSelect");
        let neighbourhoodSelect2 = document.getElementById("neighbourhoodSelect2");
        neighbourhoodSelect2.hidden = true;
        neighbourhoodSelect2.innerHTML = "";
        neighbourhoodSelect.innerHTML = "<option selected value> -- select an option -- </option>";
        fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/municipios/${idMunicipio}/distritos`)
            .then(response => response.json())
            .then(neighbourhoods => neighbourhoods.forEach(neighbourhood => {
                let neighbourhoodnew = document.createElement("option");
                neighbourhoodnew.value = neighbourhood.id;
                neighbourhoodnew.innerHTML = neighbourhood.nome;
                neighbourhoodnew.dataset.nome = neighbourhood.nome;
                neighbourhoodSelect.appendChild(neighbourhoodnew);
            }));
        neighbourhoodSelect.hidden = false;
        neighbourhoodSelect.selectedIndex = -1;
        selectFake.value = select.options[select.selectedIndex].dataset.nome;
        console.log("cty:" + selectFake.value);
    };
    
    const loadSubdistritos = async () => {
        let distrito = document.getElementById("neighbourhoodSelect");
        let neighbourhoodSelect = document.getElementById("neighbourhoodSelect2");
        neighbourhoodSelect.innerHTML = "";
        fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/distritos/${distrito.value}/subdistritos`)
            .then(response => response.json())
            .then(neighbourhoods => neighbourhoods.forEach(neighbourhood => {
                let neighbourhoodnew = document.createElement("option");
                neighbourhoodnew.value = neighbourhood.id;
                neighbourhoodnew.innerHTML = neighbourhood.nome;
                neighbourhoodnew.dataset.nome = neighbourhood.nome;
                neighbourhoodSelect.appendChild(neighbourhoodnew);
            }));
        await esperarPorTempo(1000);
        let listaChildren = neighbourhoodSelect.childNodes;
        let neighbourhoodSelectFake = document.getElementById("neighbourhoodSelectFake");
        if (neighbourhoodSelect.children.item(0)) {
            neighbourhoodSelect.hidden = false;
            neighbourhoodSelect.selectedIndex = -1;
        } else {
            neighbourhoodSelect.hidden = true;
            neighbourhoodSelectFake.value = distrito.options[distrito.selectedIndex].dataset.nome;
            console.log("nei " + neighbourhoodSelectFake.value);
        }
    };
    
    const changeFake = (node) => {
        let neighbourhoodSelectFake = document.getElementById("neighbourhoodSelectFake");
        let subdistrito = document.getElementById("neighbourhoodSelect2");
        neighbourhoodSelectFake.value = subdistrito.options[subdistrito.selectedIndex].dataset.nome;
        console.log("nei " + neighbourhoodSelectFake.value)
    };

#### - *announceEdit*
the 'POST' in its name refers to the http request type. Furthermore, it opens an edit
menu for the entity's data, using a fetch. there are other functions that help it, 
such as the *showLocation*, *showReligion* and *cancelEdit* functions, 
which will act on the appearance of the menu and its cancellation.

    const announceEdit = (event, announeId, userId) => {
        event.preventDefault();
        let text = document.getElementById("edit-text").value;
        fetch(`/edit/${announeId}`, {
            method: 'POST',
            body: JSON.stringify({
                text: text
            })
        }).then(response => response.json()).then(result => {
            console.log(result);
            document.getElementById(`${announeId}`).innerHTML = `<h3>${text}</h3>
                                                                        <p onclick="edit(${userId},${announeId})" class="btn btn, butao">Edit</p>`
        });
    };

### -holly.static.holly.styles.css
This file styles the entire project, and after that, makes the appropriate changes 
for the mobile version within *@media (max-width:1000px)*. 
I focused on a clean style with some golden details

### -holly.templates.holly
folder that contains the HTML of the pages and the templates created,
all using the django template.

These are the templates:

*-entities.html*: block that contains the standard structure of a religious
entity that appears in a search. This template is used by other pages;

*-erro.html*: generic error page that receives a message depending on the request;

*-memberOf.html*: Page that shows all entities the user is member of; 

*-index.html*: Page that allows the user to search for entities by location and religion;

*-layout.html*: Used as the default layout for all other pages;

*-login.html*: Page for the user's login;  

*-pagination.html*: block that contains the standard structure of a pagination
 that appears at the bottom of the page. This template is used by other pages;

*-announces.html*: block that contains the standard structure of an announcement 
 that appears in profile page and announcements page;

*-profile.html*: page that shows a user's data and advertisements if it is an entity.
in addition to allowing the editing of this data;

*-register.html*: page that allows user registration;

*-resultEntities.html*: page that serves as a standard for different search results for entities.

### -holly.models.py
python file that contains the classes used in the project. Being them:

*--class Religion*: class that abstracts the religions present in the project, 
currently only containing the 'name' element


    class Religion(models.Model):
       name = models.CharField(max_length=999)
       def __str__(self):
           return f"{self.name}"
*--class Location*: 
class that abstracts the cities of the state of Rio de Janeiro,
containing the elements: 'city', 'neighborhood' and 'details'

    class Location(models.Model):
        city = models.CharField(max_length=999)
        neighbourhood = models.CharField(max_length=999)
        details = models.CharField(max_length=999)
        def __str__(self):
            return f"{self.neighbourhood}"
*--class User* : 
class that abstracts users, which extends the AbstractUser class and contains the elements:

memberOf: which is a ManyToMany relationship with other
users and represents the entities that the user is a member of;

isEntity: boolean that indicates whether the user is an entity;

religions: ManyToMany with Religion objects, will only exist if the user 
is an entity;

locations: ForeignKey for a location, will only exist if the
user is an entity;

text: represents a brief description of the entity, it 
will only exist if the user is an entity;

    class User(AbstractUser):
        memberOf = models.ManyToManyField('self', blank=True, symmetrical=False)
        isEntity = models.BooleanField(default=False)
        religions = models.ManyToManyField(Religion, blank=True, symmetrical=False)
        locations = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="userEntitys", blank=True, null=True)
        text = models.CharField(max_length=999)

*--class Announce*: 
class that abstracts the announces of an entity user. containing the elements: 

user: a ForeingKey for user;

text; and date.

    class Announce(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announces")
        text = models.CharField(max_length=999)
        date = models.DateTimeField(auto_now_add=True)
        def serialize(self):
            return {
                "id": self.id,
                "user": self.user.id,
                "text": self.text,
                "date": self.date,
            }
        def __str__(self):
            return f"{self.text}"

### -holly.urls.py
File that contains the URLs (Paths) that are within the array 'urlpatterns' and can 
be accessed and activate their functions in views.py

    urlpatterns = [
        path("", views.index, name="index"),
        path("login", views.login_view, name="login"),
        path("logout", views.logout_view, name="logout"),
        path("register", views.register, name="register"),
        path("profile/<int:userId>", views.profile, name="profile"),
        path("editProfile/<int:userId>", views.editProfile, name="editProfile"),
        path("memberOf", views.memberOf, name="memberOf"),
        path("edit/<announceId>", views.edit, name="edit"),
        path("entities", views.entities, name="entities")
    ]
### -holly.views.py

File that contains the python GETs and POSTs functions that will be executed by each
part of the project, executing different functions.
These functions are:

#### - *index*: 
in POST: It will perform a search for entities filtering by location and region, in addition to being paginated.
Returning the resultEntities.html page with the title "Result of search"

in GET:
It will return to the search page

    @login_required(login_url="login")
    def index(request):
        if request.method == "POST":
            religionsSelect = request.POST["religionsSelect"]
            city = request.POST["city"]
            print(city)
            neighbourhood = request.POST["neighbourhood"]
            print(neighbourhood)
    
            religion = Religion.objects.get(name=religionsSelect)
            locations = Location.objects.all().filter(city=city, neighbourhood=neighbourhood)
            entities = User.objects.all().filter(religions=religion, locations__in=locations)
            print(religion)
            print(locations)
            print(entities.__len__())
            paginator = Paginator(entities, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "holly/resultEntities.html", {
                "entities": page_obj,
                "title": "Result of search"
            })
    
        else:
            user = User.objects.get(pk=request.user.id)
            if user.isEntity:
                return profile(request, user.id)
            else:
                return render(request, "holly/index.html")

#### - *memberOf*:
Returns all announcements from entities that the user is a member of, this is rendered on 
the memberOf.html page, in addition to being paginated

    @login_required(login_url="login")
    def memberOf(request):
        user = User.objects.get(pk=request.user.id)
        print(user.memberOf.all())
        print(user.memberOf)
        announces = Announce.objects.all().filter(user__in=user.memberOf.all()).order_by('-id')
        paginator = Paginator(announces, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "holly/memberOf.html", {
            "announces": page_obj
        })

#### - *entities*:
Returns a summary of all entities, this is rendered on 
the resultEntities.html page with "All entities" as title, in addition to being paginated

    def entities(request):
        entities = User.objects.all().filter(isEntity=True).order_by('-id')
        paginator = Paginator(entities, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "holly/resultEntities.html", {
            "entities": page_obj,
            "title": "All entities"
        })

#### - *profile*: 
in POST: First, it checks whether the user is a religious entity, if so, an announcement can be made

in GET: if the user who will have the page returned is an entity (/profile/{id}, that is, the user whose id is
in the url), Returns all the entity's announces, this is rendered in
the profile.html page, in addition to being paginated

    @login_required(login_url="login")
    def profile(request, userId):
        if request.method == "POST":
            if request.user.id == userId and User.objects.get(pk=userId).isEntity:
                text = request.POST["text"]
                if text:
                    announce = Announce(user=request.user, text=text)
                    announce.save()
                    return HttpResponseRedirect(reverse('profile', args=(userId,)))
                else:
                    return render(request, "network/erro.html", {
                        "error": "You need to put a text in the announce"
                    })
            else:
                return render(request, "holly/erro.html", {
                    "error": "Something went wrong"
                })
        else:
            if User.objects.get(pk=userId).isEntity:
                announces = Announce.objects.all().filter(user=User.objects.get(pk=userId)).order_by('-id')
                paginator = Paginator(announces, 5)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, "holly/profile.html", {
                    "announces": page_obj,
                    "profileUser": User.objects.get(pk=userId),
                    "members": User.objects.all().filter(memberOf=User.objects.get(pk=userId))
                })
            else:
                return render(request, "holly/erro.html", {
                    "error": "Something went wrong"
                })

#### - *editProfile*: 
in POST: First there is validation if the user who made the request is the same one who will have the data 
edited and if this user is a religious entity, if this is all true, the religion, description and location 
data will be changed.

    @login_required(login_url="login")
    def editProfile(request, userId):
        if request.method == "POST":
            if request.user.id == userId and User.objects.get(pk=userId).isEntity:
                user = User.objects.get(pk=userId)
    
                try:
                    religionStr = request.POST["religion"]
                    try:
                        user.religions.clear()
                        user.religions.add(Religion.objects.get(name=religionStr))
                    except:
                        religion = Religion(name=religionStr)
                        religion.save()
                        user.religions.add(religion)
                finally:
                    try:
                        city = request.POST["city"]
                        neighbourhood = request.POST["neighbourhood"]
                        details = request.POST["details"]
                        text = request.POST["text"]
                        if city and neighbourhood and details:
                            location = Location(city=city, neighbourhood=neighbourhood, details=details)
                            location.save()
                            user.locations = location
                        elif details:
                            user.locations.details = details
                            user.locations.save()
                        if text:
                            user.text = text
                    finally:
                        user.save()
                return HttpResponseRedirect(reverse('profile', args=(userId,)))
            else:
                return render(request, "holly/erro.html", {
                    "error": "Something went wrong"
                })

#### - *switch*: 
in POST: Add or remove a user from the list of members of a religious entity

    def switch(request, userId):
        if request.method == "POST":
            memberOf = request.POST["memberOf"]
            if memberOf == 'true':
                User.objects.get(pk=request.user.id).memberOf.remove(User.objects.get(pk=userId))
                return HttpResponseRedirect(reverse('profile', args=(userId,)))
            elif memberOf == 'false':
                User.objects.get(pk=request.user.id).memberOf.add(User.objects.get(pk=userId))
                return HttpResponseRedirect(reverse('profile', args=(userId,)))
            else:
                return render(request, "holly/erro.html", {
                    "error": "Something went wrong"
                })

#### - *edit*: 
in POST: Add or remove a user from the list of members of a religious entity

    @csrf_exempt
    @login_required
    def edit(request, announceId):
        if request.method == "POST":
            data = json.loads(request.body)
            announce = Announce.objects.get(pk=announceId)
            announce.text = data.get("text", "")
            announce.save()
            return JsonResponse({"message": "Announce edited successfully."}, status=200)
        else:
            announce = Announce.objects.get(pk=announceId)
            if announce:
                return JsonResponse(announce.serialize(), safe=False)
            else:
                return JsonResponse({"error": "This announce doesn't exist"}, status=400)

#### - *login_view*: 
Default login function. In the end, if the user is an entity, it will redirect to the profile page. 
If it's a normal user, it will redirect to the index page.

    def login_view(request):
        if request.method == "POST":
    
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
    
            # Check if authentication successful
            if user is not None:
                login(request, user)
                if user.isEntity:
                     return HttpResponseRedirect('profile', args=(userId,)))
                else:
                     return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "holly/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "holly/login.html")

#### - *logout_view*: 
Default logout function 

    def logout_view(request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))

#### - *register*: 
in POST: First confirm that the password and password confirmation are the same. 
After that, it checks whether the user will register as a religious entity or not. If it is a normal user,
the system creates a new user with just the name, email, password and isEntity as false.

If it is a religious entity, in addition to name, email, password and isEntity as true,
the user will have their religion added (if it does not exist, it will be created), 
and their location (another object with city, neighborhood and details).

If the user 
creation is successful and the user is an entity, it will redirect to the profile page. But
if it's a normal user, it will redirect to the index page.

in GET: renders the register.html page

    def register(request):
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
    
            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            isEntity = request.POST["isEntity"]
            if password != confirmation:
                return render(request, "holly/register.html", {
                    "message": "Passwords must match."
                })
            if isEntity == "True":
                try:
                    user = User.objects.create_user(username, email, password)
                    user.isEntity = True
                    religionStr = request.POST["religion"]
                    try:
                        user.religions.add(Religion.objects.get(name=religionStr))
                    except:
                        religion = Religion(name=religionStr)
                        religion.save()
                        user.religions.add(religion)
    
                    city = request.POST["city"]
                    neighbourhood = request.POST["neighbourhood"]
                    details = request.POST["details"]
                    location = Location(city=city, neighbourhood=neighbourhood, details=details)
                    location.save()
    
                    text = request.POST["text"]
                    user.text = text
                    user.locations = location
    
                    user.save()
                except IntegrityError:
                    return render(request, "holly/register.html", {
                        "message": "Username already taken."
                    })
                login(request, user)
                return HttpResponseRedirect('profile', args=(userId,)))
            # Attempt to create new user
            else:
                try:
                    user = User.objects.create_user(username, email, password)
                    user.isEntity = False
                    user.save()
                except IntegrityError:
                    return render(request, "holly/register.html", {
                        "message": "Username already taken."
                    })
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
    
        else:
            return render(request, "holly/register.html")

## How to run the application
First of all, install Django with pip3 install Django.

In your terminal, cd into the finalProject directory.

Run python manage.py makemigrations holly to make migrations for the holly app.

Run python manage.py migrate to apply migrations to your database.

