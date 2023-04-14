let scroll_actions = {
    percentage: 0,

    update: (event) => {
        const element = document.getElementById('show_logger');
        const actual_percentage = element.scrollTop / (element.scrollHeight - element.offsetHeight);
        if (actual_percentage < this.percentage) console.log("Going up!");
        if (actual_percentage > this.percentage) console.log("Going down!");
        scroll_actions.percentage = actual_percentage;
    }
}

let sal_index = {
    selected: null,

    update: (index) => {
        if (index === "")
            sal_index.selected = null;

        else
            sal_index.selected = index;
    },
    reset: () => {
        sal_index.selected = null;
    }
}


function select_date(new_date_str) {
    clear_accordion();
    add_information_label();
    get_log_values_from_date(new Date(new_date_str));
}

function set_events() {
    const accordionItemHeaders = document.querySelectorAll(".accordion-item-header");
    accordionItemHeaders.forEach(accordionItemHeader => {
        accordionItemHeader.addEventListener("dblclick", event => {
            // Uncomment in case you only want to allow for the display of only one collapsed item at a time!

            const currentlyActiveAccordionItemHeader = document.querySelector(".accordion-item-header.active");
            if (currentlyActiveAccordionItemHeader && currentlyActiveAccordionItemHeader !== accordionItemHeader) {
                currentlyActiveAccordionItemHeader.classList.toggle("active");
                currentlyActiveAccordionItemHeader.nextElementSibling.style.maxHeight = 0;
            }

            accordionItemHeader.classList.toggle("active");
            const accordionItemBody = accordionItemHeader.nextElementSibling;
            if (accordionItemHeader.classList.contains("active")) {
                accordionItemBody.style.maxHeight = accordionItemBody.scrollHeight + "px";
            } else {
                accordionItemBody.style.maxHeight = 0;
            }
        });
    });
}


let last_selected = null;

function set_red_color(element, text) {
    if (text.includes("exception"))
        element.style.color = "red";
    else element.style.color = "black";
}

function selected_header(header) {
    if (last_selected && last_selected.header === header) {
        header.style.color = last_selected.color;
        last_selected = null;
        return;
    }
    if (last_selected)
        last_selected.header.style.color = last_selected.color;
    last_selected = {"header": header, 'color': header.style.color};
    header.style.color = "blue";
}

function clear_accordion() {
    let accordion_element = document.getElementById('show_logger');//.forEach((elem) => elem.remove());
    while (accordion_element.firstChild) {
        accordion_element.removeChild(accordion_element.lastChild);
    }
}

function add_information_label() {
    const global_parent = document.getElementById('show_logger');
    let label = document.createElement('div');
    label.innerText = "Waiting for data";
    global_parent.appendChild(label)
}

async function add_data_to_accordion(data) {
    await new Promise(r => setTimeout(r, 2000));
    const global_parent = document.getElementById('show_logger');
    let accordion = document.createElement('div');
    accordion.className = 'accordion';
    accordion.id = 'accordion'
    for (const i in data) {
        let accordion_item = document.createElement('div');
        accordion_item.className = 'accordion-item';
        accordion.appendChild(accordion_item);

        const accordion_header = document.createElement('div');
        accordion_header.className = "accordion-item-header not-selectable";
        accordion_header.innerText = `Index: ${data[i][2]} - Timestamp: ${data[i][0].replace("GMT", "UTC")}`;
        set_red_color(accordion_header, data[i][3]);

        accordion_header.onclick = (event) => {
            selected_header(accordion_header)
        };
        accordion_item.appendChild(accordion_header);

        let accordion_body = document.createElement('div');
        accordion_body.className = 'accordion-item-body';
        accordion_item.appendChild(accordion_body);

        let accordion_body_content = document.createElement('div');
        accordion_body_content.className = 'accordion-item-body-content';
        accordion_body_content.innerText = data[i][3];
        accordion_body.appendChild(accordion_body_content);
    }
    global_parent.appendChild(accordion);
    set_events();
}


function advance_log_info() {
    const accordionItemHeaders = document.querySelectorAll(".accordion-item-header");
    let initial_index = 0;
    if (last_selected !== null) {
        initial_index = Array.from(accordionItemHeaders).indexOf(last_selected.header) + 1;
    }
    for (let index = initial_index; index < accordionItemHeaders.length; index++) {
        const accordionItemHeader = accordionItemHeaders[index];
        if (sal_index.selected === null || accordionItemHeader.innerText.includes(sal_index.selected)) {
            accordionItemHeader.click()
            setTimeout(() => {
                accordionItemHeader.scrollIntoView()
            }, "200");
            break;
        }
    }
}

function rewind_log_info() {
    const accordionItemHeaders = document.querySelectorAll(".accordion-item-header");
    let initial_index = accordionItemHeaders.length - 1;
    if (last_selected !== null) {
        initial_index = Array.from(accordionItemHeaders).indexOf(last_selected.header) - 1;
    }
    for (let index = initial_index; index >= 0; index--) {
        const accordionItemHeader = accordionItemHeaders[index];
        if (sal_index.selected === null || accordionItemHeader.innerText.includes(`Index: ${sal_index.selected}`)) {
            accordionItemHeader.scrollIntoView()
            accordionItemHeader.click();
            break;
        }
    }
}

function date_to_str(date) {
    date_list = date.toDateString().split(" ");
    return `${date_list[0]}, ${date_list[2]} ${date_list[1]} ${date_list[3]}`
}

function move_to_date(date) {
    const date_str = date_to_str(date);
    const accordionItemHeaders = document.querySelectorAll(".accordion-item-header");
    for (let index = 0; index < accordionItemHeaders.length; index++) {
        const accordionItemHeader = accordionItemHeaders[index];
        if (accordionItemHeader.innerText.includes(date_str)) {
            accordionItemHeader.click()
            accordionItemHeader.scrollIntoView();
            break;
        }
    }
}

async function get_log_values_from_date(date = new Date(),
                                        prev_delta_hours = 12,
                                        prev_delta_days = 1,
                                        post_delta_hours = 12,
                                        post_delta_days = 1) {
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const currentDate = `${year}-${month}-${day}`;
    fetch(`http://${data_sever_information._host}:${data_sever_information._port}/log_messages` + `?begin_date=${currentDate}&prev_delta_hours=${prev_delta_hours}&prev_delta_days=${prev_delta_days}&post_delta_hours=${post_delta_hours}&post_delta_days=${post_delta_days}`)
        .then((response) => response.json())
        .then((data) => add_data_to_accordion(data).then(() => move_to_date(date)))
}

async function get_last_logs(n) {
    fetch(`http://${data_sever_information._host}:${data_sever_information._port}/log_messages` + `?n=${n}`)
        .then((response) => response.json())
        .then((data) => add_data_to_accordion(data));
}

/*
<div className="accordion">
    <div className="accordion-item">
        <div className="accordion-item-header">
            What is Web Development?
        </div>
        <!-- /.accordion-item-header -->
        <div className="accordion-item-body">
            <div className="accordion-item-body-content">
                Web Development broadly refers to the tasks associated with developing functional
                websites and applications for the Internet. The web development process includes web
                design, web content development, client-side/server-side scripting and network
                security configuration, among other tasks.
            </div>
        </div>
        <!-- /.accordion-item-body -->
    </div>
    <!-- /.accordion-item -->
</div>
*/

function initialize_scroll() {
    let element = document.getElementById('show_logger');
    element.onscroll = scroll_actions.update;
    scroll_actions.percentage = element.scrollTop / (element.scrollHeight - element.offsetHeight);
    get_last_logs(5);
};

let data_sever_information = {
    _host: "127.0.0.1",
    _port: 8000,
    set_host: (host) => {
        data_sever_information.host = host;
    },
    set_port: (port) => {
        data_sever_information.port = port;
    }
}