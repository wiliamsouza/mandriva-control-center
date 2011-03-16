import Qt 4.7
import "mandriva"


Rectangle {
    width: 300
    height: 200

    MdvTextInput {
        id: text1
        onTextChanged: text2.text = "/home/" + text
    }

    MdvTextInput {
        id: text2
        text: "/home/"
        x: 0
        y: 37

    }

    ListModel {
        id: shellModel
        ListElement {
            content: "/bin/bash"
            icon: ""
        }

        ListElement {
            content: "/bin/dash"
            icon: ""
        }

        ListElement {
            content: "/bin/sh"
            icon: ""
        }
    }
}
