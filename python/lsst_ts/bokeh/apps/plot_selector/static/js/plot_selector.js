
const plotController = {
    _menu_mouse_over: () => {
        document.getElementById("plot_menu").style.width = "5%";
    },

    _menu_mouse_out: () => {
        document.getElementById("plot_menu").style.width = "0.3%";
    },
    plot_code: `<div id="plot_menu" onmouseover="this._menu_mouse_over()" onmouseout="this._menu_mouse_out()" 
                    style="background-color: black; transition: all .1s linear; width:0.3%;">    
                </div>
               <div id="plot" style="width: 99.9%; background-color: grey"></div>`,

    plus_click: (event) => {
        fetch("http://localhost:8000/plot_selector/one_variable")
            .then((response) => response.json())
            .then((item) => {
                const element = document.getElementById('plot_box_3_1');
                element.style.justifyContent = "normal";
                element.innerHTML = this.plot_code;
                Bokeh.embed.embed_item(item, "plot");
            });
    },
    create_plot_link : () => {
        const global_parent = document.getElementById(this.link_id);
        global_parent.onclick = this.plus_click;
    },
    linked_element: ""
}

const plot_controllers_relation = {}


function create_plot_controller(linked_element) {
    const new_plot_controller = Object.create(plotController)
    new_plot_controller.linked_element = linked_element;
    new_plot_controller.create_plot_link();
    plot_controllers_relation.link_id = new_plot_controller;
}

function initialize() {


}