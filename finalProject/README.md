# HOLLY.APP
#### Video Demo: TODO
#### Description:
hello, my name is Pedro vieira, I speak from Rio de Janeiro, Brazil, and this is my 
final project of CS50’s Web Programming with Python and JavaScript.
my project is called Holly.app,
it takes that name because my project aims to facilitate the activities of religious entities in 'Rio de janeiro', 
such as churches, synagogues, mosques, etc. It focuses mainly on the findability of these entities and their 
communication with the faithful.
all project was made in Django(python) for the back-end, and HTML5/CSS3/JS without any framework, only the CSS bootstrap, for front-end and SQLite for manage the database.

## SUMMARY
My program helps religious entities communicate with their followers;
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

    const edit = (userId, postId) => {
        postId = parseInt(postId);
        userId = parseInt(userId);
        fetch(`/edit/${postId}`)
            .then(response => response.json())
            .then(post => {
                if (post.user == userId) {
                    document.getElementById(post.id).innerHTML = `
                    <form>
                    <textarea name="text" rows="4" style="width: 100%" id ="edit-text">${post.text}</textarea>
                    <br>
                    <input type="submit" class="btn btn, butao" onclick="editPost(event, ${postId}, ${userId})" value="Edit">
                    </form>`;
                } else {
                    document.getElementById(post.id).innerHTML = "ERROR";
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

#### - *editPost*
the 'POST' in its name refers to the http request type. Furthermore, it opens an edit
menu for the entity's data, using a fetch. there are other functions that help it, 
such as the *showLocation*, *showReligion* and *cancelEdit* functions, 
which will act on the appearance of the menu and its cancellation.

    const editPost = (event, postId, userId) => {
        event.preventDefault();
        let text = document.getElementById("edit-text").value;
        fetch(`/edit/${postId}`, {
            method: 'POST',
            body: JSON.stringify({
                text: text
            })
        }).then(response => response.json()).then(result => {
            console.log(result);
            document.getElementById(`${postId}`).innerHTML = `<h3>${text}</h3>
                                                                        <p onclick="edit(${userId},${postId})" class="btn btn, butao">Edit</p>`
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

*-following.html*: Page that shows all entities the user is member of; 

*-index.html*: Page that allows the user to search for entities by location and religion;

*-layout.html*: Used as the default layout for all other pages;

*-login.html*: Page for the user's login;  

*-pagination.html*: block that contains the standard structure of a pagination
 that appears at the bottom of the page. This template is used by other pages;

*-posts.html*: block that contains the standard structure of an announcement 
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

following: which is a ManyToMany relationship with other
users and represents the entities that the user is a member of;

isEntity: boolean that indicates whether the user is an entity;

religions: ManyToMany with Religion objects, will only exist if the user 
is an entity;

locations: ForeignKey for a location, will only exist if the
user is an entity;

text: represents a brief description of the entity, it 
will only exist if the user is an entity;

    class User(AbstractUser):
        following = models.ManyToManyField('self', blank=True, symmetrical=False)
        isEntity = models.BooleanField(default=False)
        religions = models.ManyToManyField(Religion, blank=True, symmetrical=False)
        locations = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="userEntitys", blank=True, null=True)
        text = models.CharField(max_length=999)

*--class Post*: 
class that abstracts the announces of an entity user. containing the elements: 

user: a ForeingKey for user;

text; and date.

    class Post(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
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











