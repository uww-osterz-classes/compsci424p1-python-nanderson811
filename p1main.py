# Noah Anderson

v1_pcb = []
v2_pcb = []

import time

class V1PCB:
    def __init__(self, parent=None):
        self.__children = []
        self.__parent = parent

    def get_parent(self):
        return self.__parent

    def get_children(self):
        return self.__children

    def add_child(self, child):
        self.__children.append(child)

    def remove_child(self, child):
        self.__children.remove(child)


class V1PCBArray:
    def __init__(self, pcb_array):
        self.__pcb_array = pcb_array

    def create(self, parent_pid):
        if len(self.__pcb_array) == 0:
            new_process = V1PCB(-1)
            self.__pcb_array.append(new_process)
        else:
            new_process = V1PCB(parent_pid)
            self.__pcb_array.append(new_process)
            self.__pcb_array[new_process.get_parent()].add_child(self.__pcb_array.index(new_process))

    def destroy(self, target_pid):
        for child in self.__pcb_array[target_pid].get_children():
            child_process = self.__pcb_array[child]
            self.destroy(self.__pcb_array.index(child_process))
            self.__pcb_array.remove(child_process)

    def showProcessInfo(self):
        index = 0
        for process in self.__pcb_array:
            output_str = ""
            output_str += "Process: " + str(index) + ": parent is "
            output_str += str(process.get_parent()) + " and children are "
            if len(process.get_children()) == 0:
                output_str += "empty"
            else:
                for x in process.get_children():
                    output_str += str(x) + " "
            print(output_str)
            index += 1



class V2PCB:
    def __init__(self, parent=None):
        self.__parent = parent
        self.__child = None
        self.__older_sibling = None
        self.__younger_sibling = None

    def get_parent(self):
        return self.__parent

    def get_first_child(self):
        return self.__child

    def get_younger_sibling(self):
        return self.__younger_sibling

    def get_older_sibling(self):
        return self.__older_sibling

    def set_first_child(self, child):
        self.__child = child

    def set_older_sibling(self, older_sibling):
        self.__older_sibling = older_sibling

    def set_younger_sibling(self, younger_sibling):
        self.__younger_sibling = younger_sibling


class V2PCBArray:
    def __init__(self, pcb_array):
        self.__pcb_array = pcb_array

    def create(self, parent_pid):
        try:
            if len(self.__pcb_array) < parent_pid-1:
                print("Error: Parent Process ID Not found, create command cancelled.")
                return

            if len(self.__pcb_array) == 0:
                new_process = V2PCB(-1)
            else:
                new_process = V2PCB(parent_pid)

            self.__pcb_array.append(new_process)

            if len(self.__pcb_array) == 1:
                return

            if parent_pid < 0:
                return
            else:
                pid = self.__pcb_array.index(new_process)
                process_parent = self.__pcb_array[new_process.get_parent()]

            if process_parent.get_first_child() is None:
                process_parent.set_first_child(pid)
            else:
                current_child = self.__pcb_array[process_parent.get_first_child()]
                while current_child.get_younger_sibling() is not None:
                    current_child = current_child.get_younger_sibling()

                current_child.set_younger_sibling(pid)
                new_process.set_older_sibling(self.__pcb_array.index(current_child))
        except IndexError:
            print("Error: Parent process not found, create command skipped.")

    def destroy(self, target_pid, is_child=0):
        target_process = self.__pcb_array[target_pid]

        parent = self.__pcb_array[target_process.get_parent()]

        if target_process.get_first_child() is not None:
            child_process = self.__pcb_array[target_process.get_first_child()]
            child_process_index = self.__pcb_array.index(child_process)
            self.destroy(child_process_index, 1)
        if target_process.get_younger_sibling() is not None and is_child == 1:
            younger_sibling_process = self.__pcb_array[target_process.get_younger_sibling()]
            younger_sibling_index = self.__pcb_array.index(younger_sibling_process)
            self.destroy(younger_sibling_index, 1)

        if target_process.get_younger_sibling() is None:
            new_first_child = None
        else:
            new_first_child = self.__pcb_array[target_process.get_younger_sibling()]

        self.__pcb_array.pop(target_pid)

        if new_first_child:
            new_first_child.set_older_sibling(None)
            parent.set_first_child(self.__pcb_array.index(new_first_child))
        else:
            parent.set_first_child(None)

    def showProcessInfo(self):
        index = 0
        for process in self.__pcb_array:
            output_str = ""
            output_str += "Process: " + str(index) + ": parent is "
            output_str += str(process.get_parent()) + " and children are "
            if process.get_first_child() is None:
                output_str += "empty"
            else:
                output_str += str(process.get_first_child()) + " "
                current_child = self.__pcb_array[process.get_first_child()]
                while current_child.get_younger_sibling() is not None:
                    output_str += str(current_child.get_younger_sibling()) + " "
                    current_child = self.__pcb_array[current_child.get_younger_sibling()]
            print(output_str)
            index += 1


action_list = []
userinput = input("Enter a command: ")
while userinput.lower() != "end":
    parsed_input = userinput.split()
    try:
        if parsed_input[0].lower() == "create":
            create_action = ["create", int(parsed_input[1])]
            action_list.append(create_action)
            userinput = input("Enter a command: ")
        elif parsed_input[0].lower() == "destroy":
            destroy_action = ["destroy", int(parsed_input[1])]
            action_list.append(destroy_action)
            userinput = input("Enter a command: ")
        else:
            print("Error: Command not recognized")
            userinput = input("Enter a command: ")
    except ValueError:
        print("Error: Command must be in format 'create/destroy x or end' where x is an integer")
        userinput = input("Enter a command: ")

v1 = V1PCBArray([])
v2 = V2PCBArray([])
print("Version 1\n")
for x in action_list:
    if x[0] == "create":
        v1.create(x[1])
    elif x[0] == "destroy":
        v1.destroy(x[1])
    v1.showProcessInfo()
    print("\n\n")

print("Version 2\n")
for x in action_list:
    if x[0] == "create":
        v2.create(x[1])
    elif x[0] == "destroy":
        v2.destroy(x[1])
    v2.showProcessInfo()
    print("\n\n")

start_time = time.time()

for y in range(200):
    v1 = V1PCBArray([])
    for x in action_list:
        if x[0] == "create":
            v1.create(x[1])
        elif x[0] == "destroy":
            v1.destroy(x[1])

end_time = time.time()
v1.showProcessInfo()
print("Elapsed time for Version 1: " + str(end_time-start_time) + " seconds")
print("\n\n")

start_time = time.time()
for y in range(200):
    v2 = V2PCBArray([])
    for x in action_list:
        if x[0] == "create":
            v2.create(x[1])
        elif x[0] == "destroy":
            v2.destroy(x[1])

end_time = time.time()
v2.showProcessInfo()
print("Elapsed time for Version 2: " + str(end_time-start_time) + " seconds")

