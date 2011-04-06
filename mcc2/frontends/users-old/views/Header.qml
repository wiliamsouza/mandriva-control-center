//import Qt 4.7
import QtQuick 1.0

// ** Not used variable scope problem **

Component {
    //id: listViewHeader
    ButtonGroup {
        width: col.width
        height: col.height
        Column {
            id: col
            Row {
                Button {
                    text: "Users"
                    checkable: true
                    checked: true
                    onClicked: {
                        listView.model = usersModel
                        listView.delegate = userDelegate
                        groupForm.visible = false
                        userForm.visible = true

                    }
                }
                Button {
                    text: "Groups"
                    checkable: true
                    onClicked: {
                        listView.model = groupsModel
                        listView.delegate = groupDelegate
                        userForm.visible = false
                        groupForm.visible = true
                    }
                }
            }
            Entry {
                id: searchBox
                width: listView.width
                height: 28
                hint: "Search"
                leftIconSource: "images/system-search.png";
                onLeftIconClicked: searchBox.hint = "Searching...";
                rightIconSource: "images/edit-delete.png";
                onRightIconClicked: searchBox.hint = "Search";
            }
        }
    }
}
