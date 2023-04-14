
const plotController = {
    _menu_mouse_over() {
        document.getElementById("plot_menu").style.width = "5%";
    },

    _menu_mouse_out() {
        document.getElementById("plot_menu").style.width = "0.3%";
    },
    create_plot_code(item_name) {
        const plot_code = `<div id="plot_menu_${item_name}" onmouseover="this._menu_mouse_over()" onmouseout="this._menu_mouse_out()" 
                    style="background-color: black; transition: all .1s linear; width:1%;">    
                    </div>
                    <div id="plot_${item_name}" style="width: 100%; background-color: grey"></div>`
        return plot_code;
    },

    plus_click(element){
        fetch("http://localhost:8000/examples/flask_bokeh_full/widget")
            .then((response) => response.json())
            .then((item) => {
                console.log(element.className);
                const box = element.getElementsByClassName("plot_box");
                console.log(box[0].className)
                element.style.justifyContent = "normal";
                element.innerHTML = this.create_plot_code(element.className);
                Bokeh.embed.embed_item(item, `plot_${element.className}`);
            });
    },
        linked_element: "",
    create_plot_link(){
        const plus_element = this.linked_element.getElementsByClassName("plus");
        plus_element[0].addEventListener('click', () => {this.plus_click(this.linked_element)});
    }
}

const plot_controllers_relation = {}


function create_plot_controller(linked_element) {
    const new_plot_controller = Object.create(plotController)
    new_plot_controller.linked_element = linked_element;
    new_plot_controller.create_plot_link();
    plot_controllers_relation.link_id = new_plot_controller;
}

function initialize() {
    const container = document.getElementById("plot_container");
    create_plot_controller(container)
}