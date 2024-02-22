# Noah Anderson

import time


class PCBV1:
    generated_pid = 0

    # constructor, default parent is set to None for the root PCB
    def __init__(self, pid, parent=None):
        self.pid = pid
        self.children = []
        self.parent = parent

    @staticmethod
    def generate_pid():
        PCBV1.generated_pid += 1
        return PCBV1.generated_pid

    # creates a process and assigns a parent to it, and becomes a child of that parent process
    def create(self, parent_pid):
        pid = self.generate_pid()
        parent = self.find_process(parent_pid)
        if parent:
            child = PCBV1(pid, parent)
            parent.children.append(child)
            return child
        else:
            print("Parent \"" + str(parent_pid) + "\" not found.")
            return None

    # recursively destroys the children of the target_pid then removes itself from the PCB
    def destroy(self, target_pid):
        process = self.find_process(target_pid)
        if process:
            for child in process.children:
                if len(child.children) == 0:
                    child.parent.children.remove(child)
                    return
                else:
                    child.destroy(child.pid)
            process.parent.children.remove(process)
        else:
            print("Process \"" + str(target_pid) + "\" not found.")

    # navigates to root node, then searches the PCB tree
    def find_process(self, pid):
        process = self
        while process.parent:
            process = process.parent

        return process.search_tree(process, pid)

    # function to search the PCB tree for the target PID
    def search_tree(self, process, target):
        if process.pid == target:
            return process

        for child in process.children:
            child_process = self.search_tree(child, target)
            if child_process:
                return child_process

        return None

    def showProcessInfo(self):
        children_info = ""
        if len(self.children) != 0:
            children_str = ""
            for child in self.children:
                children_str += str(child.pid) + " "
                if len(child.children) == 0:
                    return "Process " + str(child.pid) + ": parent is " + str(child.parent.pid) + " and has no children"
                else:
                    children_info += child.showProcessInfo() + "\n"
            if self.parent is None:
                return "Process " + str(self.pid) + ": parent is -1 and children are " + children_str
            else:
                return "Process " + str(self.pid) + ": parent is " \
                                                    "" + str(self.parent.pid) + " and children are " + children_str
        else:
            if self.parent is None:
                return "Process " + str(self.pid) + ": parent is -1 and has no children"
            else:
                return "Process " + str(self.pid) + ": parent is " + str(self.parent.pid) + " and has no children"


class PCBV2:
    generated_pid = 0

    def __init__(self, pid, parent=None, older_sibling=None):
        self.pid = pid
        self.parent = parent
        self.first_child = None
        self.older_sibling = older_sibling
        self.younger_sibling = None

    @staticmethod
    def generate_pid():
        PCBV1.generated_pid += 1
        return PCBV1.generated_pid

    def create(self, parent_pid):
        pid = self.generate_pid()
        process = self.find_process(parent_pid)
        if process:
            if process.first_child is None:
                child = PCBV2(pid, process)
                return child
            else:
                older_sibling = process.first_child
                while older_sibling.younger_sibling is not None:
                    older_sibling = older_sibling.younger_sibling
                child = PCBV2(pid, process, older_sibling)
                older_sibling.younger_sibling = child
                return child
        else:
            print("Parent \"" + str(parent_pid) + "\" not found.")
            return None

    def destroy(self, target_pid):
        process = self.find_process(target_pid)
        if process and not process.parent:
            if process.first_child is None:
                process.older_sibling.younger_sibling = process.younger_sibling
            else:
                process.destroy(process.first_child.pid)
        else:
            print("Process \"" + str(target_pid) + "\" not found.")
            return None

        # destroys all siblings/children of target_pid by removing all references to the process
        if process.parent:
            if process.first_child is None:
                process.parent = None
            if process.younger_sibling is None:
                return None
            else:
                process.destroy(process.first_child.pid)

    # function to find if a process id is present within the PCB
    def find_process(self, pid):
        # case if PCB is empty
        if self is None:
            return None

        # case if current node is the target PID
        if self.pid == pid:
            return self

        # if node has a parent, traverses up the PCB tree until the root node
        if self.parent:
            return self.parent.find_process(pid)

        # checks older sibling recursively (if one exists) for target PID
        process = self.older_sibling.find_process(pid) if self.older_sibling else None
        if process:
            return process

        # checks younger sibling recursively (if one exists) for target PID
        process = self.younger_sibling.find_process(pid) if self.younger_sibling else None
        if process:
            return process

        # checks first child recursively (if one exists) for target PID
        process = self.first_child.find_process(pid) if self.first_child else None
        if process:
            return process

        return None

    def show_process_info_root(self):
        current_process = self
        while current_process.parent:
            current_process = current_process.parent

        return current_process.showProcessInfo()

    def showProcessInfo(self):
        message = ""
        if self.parent is None:
            message = "Process " + str(self.pid) + ": parent is -1 and children are "
            children_string = "empty"
            if self.first_child:
                children_string = str(self.first_child.pid) + " "
                child = self.first_child
                while child.younger_sibling:
                    children_string += str(child.younger_sibling.pid) + " "
                    child = child.younger_sibling
            message += children_string + "\n"
            if self.first_child:
                message += self.first_child.showProcessInfo()
            return message
        else:
            message += "Process " + str(self.pid) + ": parent is " + str(self.parent.pid) + " and children are "
            children_string = "empty"
            if self.first_child:
                children_string = str(self.first_child.pid) + " "
                child = self.first_child
                while child.younger_sibling:
                    children_string += str(child.younger_sibling.pid) + " "
                    child = child.younger_sibling
            message += children_string + "\n"
            if self.younger_sibling:
                message += self.younger_sibling.showProcessInfo()
            elif self.first_child:
                message += self.first_child.showProcessInfo()
            else:
                return message


# Command sequence storage
command_sequence = []

# Accepting commands
while True:
    command = input("Enter command (create N, destroy N, or end): ").strip().lower()
    if command == "end" or not command.startswith(("create", "destroy")):
        break
    else:
        try:
            action, number = command.split()
            if action == "create":
                number = int(number)
            command_sequence.append((action, number))
        except ValueError:
            print("Invalid command. Please enter commands in the format 'create N' or 'destroy N'.")

# Creating objects
v1 = PCBV1(1)
v2 = PCBV2(1)

# Running command sequence once for each version
for action in command_sequence:
    cmd, n = action
    if cmd == "create":
        v1.create(n)
        v2.create(n)
    elif cmd == "destroy":
        v1.destroy(n)
        v2.destroy(n)
    print("Version 1:")
    # v1.showProcessInfo()
    print("Version 2:")
    v2.show_process_info_root()

    # Running command sequence 200 times for Version 1
start_time_v1 = time.time()
for _ in range(200):
    for action in command_sequence:
        cmd, n = action
        if cmd == "create":
            v1.create(n)
        elif cmd == "destroy":
            v1.destroy(n)
end_time_v1 = time.time()
v1_running_time = end_time_v1 - start_time_v1
print(f"Version 1 running time: {v1_running_time} seconds")

# Running command sequence 200 times for Version 2
start_time_v2 = time.time()
for _ in range(200):
    for action in command_sequence:
        cmd, n = action
        if cmd == "create":
            v2.create(n)
        elif cmd == "destroy":
            v2.destroy(n)
end_time_v2 = time.time()
v2_running_time = end_time_v2 - start_time_v2
print(f"Version 2 running time: {v2_running_time} seconds")
