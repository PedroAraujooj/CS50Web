let select = document.getElementById("localSelect");
let selectFake = document.getElementById("localSelectFake");

window.addEventListener('load', function () {
    carregarLugares();
});
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


const changerRegisterEntity = (node) =>{
    let registerEntity = document.getElementById("registerEntity");
    if(node.value == "True"){
        registerEntity.hidden = false;
    }
    else if(node.value == "False"){
        registerEntity.hidden = true;
    }
};

function esperarPorTempo(tempoEmMilissegundos) {
    return new Promise(resolve => {
        setTimeout(resolve, tempoEmMilissegundos);
    });
}

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

const showReligion = (event, buttom) =>{
    buttom.hidden = true;
    event.preventDefault();
  document.getElementById('showReligion').innerHTML = `<label for='religion'>Change your religion: </label><br>
            <select name='religion' id='religionsSelect'>
                <option value='Protestantism'>Protestantism</option>
                <option value='Catholicism'>Catholicism</option>
                <option value='Islam'>Islam</option>
                <option value='Judaism'>Judaism</option>
                <option value='Afro'>African religions</option>
            </select><br>`;
      document.getElementById('showReligion').hidden = false;

};

const showLocation = (event, buttom) =>{
    buttom.hidden = true;
    event.preventDefault();
    document.getElementById('showLocation').hidden = false;
    document.getElementById('showSummary').hidden = false;
    document.getElementById('showSubmit').hidden = false;
    carregarLugares();
};

const showAnnounce = (event, buttom) =>{
    buttom.hidden = true;
    event.preventDefault();
    document.getElementById('divAnnounce').hidden = false;
};

const cancelEdit = (event) =>{
    event.preventDefault();
    document.getElementById("editButton").hidden = false;
    document.getElementById('showLocation').hidden = true;
    document.getElementById('showSummary').hidden = true;
    document.getElementById('showSubmit').hidden = true;
    document.getElementById('showReligion').hidden = true;
};

const cancelAnnounce = (event) =>{
    event.preventDefault();
    document.getElementById("announceButton").hidden = false;
    document.getElementById('divAnnounce').hidden = true;
};