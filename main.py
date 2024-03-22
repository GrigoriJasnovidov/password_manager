import customtkinter as ctk
from customtkinter import CTkLabel as Label
from customtkinter import CTkFrame as Frame
from customtkinter import CTkEntry as Entry
from customtkinter import CTkButton as Button
from customtkinter import CTkInputDialog as InputDialog
from customtkinter import CTkScrollableFrame as ScrollableFrame

from shifr import Shifr, make_verification_key, check_correct_shifr
from utils import make_formatted_key
from verification import check_credentials
from generate_pwd import make_pwd
from utils import check_file_is_empty, get_lines_for_output, remove_line, remove_last_line, add_line, approve_adding, \
    check_key_correctness


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.file_pwds = 'passwords.gpwd'
        self.file_key = 'master-key.gpwd'
        self.verification_key_string = 'Password_2024'
        open(self.file_pwds, 'a').close()
        open(self.file_key, 'a').close()
        self.title("Grisha Passwords")
        self.geometry("1500x1200")
        self.resizable(False, False)

        self.user_frame = Frame(master=self)
        self.user_frame.grid(row=2, column=1, pady=(10, 10))
        self.output_frame = Frame(master=self)
        self.output_frame.grid(row=3, column=1, pady=(10, 10))

        # user
        entry_width = 700
        self.label_alias = Label(master=self.user_frame, text='Alias:')
        self.label_alias.grid(row=1, column=1, pady=(10, 10), padx=(10, 10))
        self.entry_alias = Entry(master=self.user_frame, width=entry_width)
        self.entry_alias.grid(row=1, column=2, pady=(10, 10), padx=(10, 10))

        self.label_url = Label(master=self.user_frame, text='Url:')
        self.label_url.grid(row=2, column=1, pady=(10, 10), padx=(10, 10))
        self.entry_url = Entry(master=self.user_frame, width=entry_width)
        self.entry_url.grid(row=2, column=2, pady=(10, 10), padx=(10, 10))

        self.label_login = Label(master=self.user_frame, text='Login:')
        self.label_login.grid(row=3, column=1, pady=(10, 10), padx=(10, 10))
        self.entry_login = Entry(master=self.user_frame, width=entry_width)
        self.entry_login.grid(row=3, column=2, pady=(10, 10), padx=(10, 10))

        self.button_add_pwd = Button(master=self.user_frame, text='Add Password', height=120, command=self.add_pwd)
        self.button_add_pwd.grid(row=5, column=3, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.button_get_pwd = Button(master=self.user_frame, text='Get Password', height=120,
                                     command=self.get_pwd)
        self.button_get_pwd.grid(row=5, column=4, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.button_show_last_pwd = Button(master=self.user_frame, text='Show Last Password', height=120,
                                           command=self.show_last_pwd)
        self.button_show_last_pwd.grid(row=5, column=5, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.button_add_pwd = Button(master=self.user_frame, text='Clear', command=self.clear)
        self.button_add_pwd.grid(row=1, column=4, rowspan=3, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.button_add_pwd = Button(master=self.user_frame, text='Exit', command=self.destroy,
                                     fg_color='red')
        self.button_add_pwd.grid(row=1, column=5, rowspan=3, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.print_pwds = Button(master=self.user_frame, text='Decrypt All Passwords', command=self.decrypt)
        self.print_pwds.grid(row=1, column=3, rowspan=3, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.button_rm_last_pwd = Button(master=self.user_frame, text='Remove Last Password', height=120,
                                         command=self.rm_last_pwd)
        self.button_rm_last_pwd.grid(row=6, column=3, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.button_rm_pwd = Button(master=self.user_frame, text='Remove Password', height=120, command=self.rm_pwd)
        self.button_rm_pwd.grid(row=6, column=4, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.button_connect = Button(master=self.user_frame, text='Change Master-Key', height=120,
                                     command=self.change_master_key)
        self.button_connect.grid(row=6, column=5, sticky='nsew', pady=(10, 10), padx=(10, 10))

        self.label_communication = Label(master=self.user_frame, text='Out')
        self.label_communication.grid(row=7, column=1)
        self.entry_communication = Entry(master=self.user_frame)
        self.entry_communication.grid(row=7, column=2, columnspan=10, sticky='nsew', pady=(10, 10), padx=(10, 10))

        # output
        self.output_scrframe = ScrollableFrame(master=self.output_frame, width=1460, height=650)
        self.output_scrframe.grid(row=1, column=1, rowspan=10, sticky='nsew', pady=(10, 10), padx=(10, 10))
        self.pwds_frames = None

    def clear(self):
        """Clear outputs off all frames."""
        self.clear_decrypted_pwds()
        self.clear_entries()
        self.entry_communication.delete(0, 'end')

    def clear_decrypted_pwds(self):
        """Clear all decrypted passwords."""
        if self.pwds_frames is not None:
            for frame in self.pwds_frames:
                frame.delete(0, 'end')
                frame.grid_forget()
                del frame
        self.pwds_frame = None

    def clear_last_decrypted_pwd(self):
        """Clear last decrypted password."""
        if self.pwds_frames is not None:
            self.pwds_frames[-1].delete(0, 'end')
            self.pwds_frames[-1].grid_forget()
            self.pwds_frames = self.pwds_frames[:-1]

    def clear_entries(self):
        """Clear alias, url and login entries."""
        self.entry_alias.delete(0, 'end')
        self.entry_url.delete(0, 'end')
        self.entry_login.delete(0, 'end')

    def communication_message(self, message: str):
        """Clear and then show message in user-communication frame.

        Args:
            message - message."""
        self.entry_communication.delete(0, 'end')
        self.entry_communication.insert(0, message)

    def decrypt(self):
        """Decrypt all encrypted passwords and then show them."""
        if check_file_is_empty(file_name=self.file_pwds):
            self.clear_decrypted_pwds()
            self.communication_message(f'The password-file {self.file_pwds} is empty.')

        else:
            dialog = InputDialog(text="Master-key:", title="Key")
            key = dialog.get_input()

            shifr = check_correct_shifr(key=key, file_pwds=self.file_pwds, file_key=self.file_key,
                                        verification_key_string=self.verification_key_string)
            if shifr:
                text = shifr.get_decrypted_pwds()
                self.clear_decrypted_pwds()
                self.show_pwds(text)
            else:
                self.communication_message(f'{key} is incorrect key or password file is damaged.')

    def show_pwds(self, text: str):
        """Builds frames for decrypted passwords and then shows passwords.

        Args:
            text: text with decrypted passwords."""
        if text != '':
            formatted_text = get_lines_for_output(text)
            length = len(formatted_text)

            self.pwds_frames = [Entry(master=self.output_scrframe, width=1400) for _ in range(length)]
            for i in range(length):
                self.pwds_frames[i].grid(row=i + 1, column=1, sticky='nsew', pady=(5, 5), padx=(5, 5))
                self.pwds_frames[i].insert(0, formatted_text[i])

    def add_pwd(self):
        """Add password if does not already exist."""
        alias = str(self.entry_alias.get())
        url = str(self.entry_url.get())
        login = str(self.entry_login.get())
        message = check_credentials(alias=alias, url=url, login=login)

        if message != 'Credentials are correct.':
            self.communication_message(message)

        else:
            dialog = InputDialog(text="Master-key:", title="Key")
            key = dialog.get_input()
            shifr = check_correct_shifr(key=key, file_pwds=self.file_pwds, file_key=self.file_key,
                                        verification_key_string=self.verification_key_string)
            if shifr:
                with open(self.file_pwds, 'r') as f:
                    encrypted_pwds = f.read()
                if encrypted_pwds == '':
                    new_pwd = shifr.build_pwd(alias=alias, url=url, login=login)
                    add_line(file_name=self.file_pwds, string=new_pwd)
                    self.communication_message('Password is successfully added.')
                    self.clear_entries()
                else:
                    decrypted_pwds = shifr.decrypt_text(encrypted_pwds)
                    if approve_adding(text=decrypted_pwds, url=url, login=login):
                        new_pwd = shifr.build_pwd(alias=alias, url=url, login=login)
                        add_line(file_name=self.file_pwds, string=new_pwd)
                        self.communication_message('Password is successfully added.')
                        self.clear_entries()
                    else:
                        self.communication_message(f'Password with url {url} and login {login} is already added.')
            else:
                self.communication_message(f'{key} is incorrect key or password file is damaged.')

    def show_last_pwd(self):
        """Show last password."""
        dialog = InputDialog(text="Master-key:", title="Key")
        key = dialog.get_input()
        shifr = check_correct_shifr(key=key, file_pwds=self.file_pwds, file_key=self.file_key,
                                    verification_key_string=self.verification_key_string)
        if shifr:
            text = shifr.get_decrypted_pwds()
            last_pwd = get_lines_for_output(text)[-1]
            self.communication_message(last_pwd)
        else:
            self.communication_message(f'{key} is incorrect key or password file is damaged.')

    def get_pwd(self):
        """Get automatically generated password provided url and login.

        The password is not necessary written in encrypted file."""
        url = self.entry_url.get()
        login = self.entry_login.get()
        message = check_credentials(alias='a', url=url, login=login)
        self.entry_alias.delete(0, 'end')
        if message != 'Credentials are correct.':
            self.communication_message(message)
        else:
            dialog = InputDialog(text="Master-key:", title="Key")
            key = dialog.get_input()
            shifr = check_correct_shifr(key=key, file_pwds=self.file_pwds, file_key=self.file_key,
                                        verification_key_string=self.verification_key_string)
            if shifr:
                proceed, formatted_key = make_formatted_key(key)
                auto_pwd = make_pwd(url=url, login=login, key=formatted_key)
                self.communication_message(auto_pwd)
            else:
                self.communication_message(f'{key} is incorrect key.')

    def rm_last_pwd(self):
        """Remove last password."""
        if check_file_is_empty(file_name=self.file_pwds):
            self.communication_message(f'The password-file {self.file_pwds} is empty.')
        else:
            dialog = InputDialog(text="Master-key:", title="Key")
            key = dialog.get_input()
            shifr = check_correct_shifr(key=key, file_pwds=self.file_pwds, file_key=self.file_key,
                                        verification_key_string=self.verification_key_string)
            if shifr:
                remove_last_line(file_name=self.file_pwds)
                self.clear_last_decrypted_pwd()
                self.communication_message('The last password is deleted successfully.')
            else:
                self.communication_message(f'{key} is incorrect key.')

    def rm_pwd(self):
        """Remove password with given url and login."""
        dialog = InputDialog(text="Master-key:", title="Key")
        key = dialog.get_input()
        shifr = check_correct_shifr(key=key, file_pwds=self.file_pwds, file_key=self.file_key,
                                    verification_key_string=self.verification_key_string)
        if shifr:

            dialog_url = InputDialog(text="Url:", title="Url")
            url = dialog_url.get_input()

            dialog_login = InputDialog(text="Login:", title="Login")
            login = dialog_login.get_input()

            text = shifr.get_decrypted_pwds()
            deleted, new_text = remove_line(text=text, url=url, login=login)
            if deleted:
                if new_text == '':
                    encrypted_text = ''
                else:
                    encrypted_text = shifr.encrypt_text(text=new_text)
                with open(self.file_pwds, 'w') as f:
                    f.writelines(encrypted_text)
                self.communication_message(f'The password with url {url} and login {login} is deleted successfully.')
            else:
                self.communication_message(f'Password with url {url} and login {login} does not exist.')
            self.clear_decrypted_pwds()
            self.show_pwds(new_text)
        else:
            self.communication_message(f'{key} is incorrect key.')

    def change_master_key(self):
        """Change master-key.

        Reencrypt files with password and master-key."""
        dialog = InputDialog(text="Master-key:", title="Key")
        key = dialog.get_input()
        shifr = check_correct_shifr(key=key, file_pwds=self.file_pwds, file_key=self.file_key,
                                    verification_key_string=self.verification_key_string)
        if shifr:
            dialog = InputDialog(text="Type new master-key", title="Ney master-key")
            new_key = dialog.get_input()
            message = check_key_correctness(new_key)
            if message != 'Key is correct.':
                self.communication_message(message)
            else:
                dialog = InputDialog(text="Type new master-key again", title="Repeat master-key")
                key2 = dialog.get_input()
                if key2 != new_key:
                    self.communication_message("Initial and repeated keys do not match. Try again.")
                else:
                    new_encrypted_key = make_verification_key(key=new_key, string=self.verification_key_string)
                    if check_file_is_empty(self.file_pwds):
                        with open(self.file_key, 'w') as f:
                            f.write(new_encrypted_key)
                    else:
                        with open(self.file_pwds, 'r') as f:
                            old_encrypted_pwds = f.read()
                        old_decrypted_pwds = shifr.decrypt_text(text=old_encrypted_pwds)
                        with open(self.file_key, 'w') as f:
                            f.write(new_encrypted_key)
                        new_shifr = Shifr(key=new_key, file_pwds=self.file_pwds, file_key=self.file_key,
                                          verification_key_string=self.verification_key_string)
                        new_encrypted_pwds = new_shifr.encrypt_text(text=old_decrypted_pwds)
                        with open(self.file_pwds, 'w') as f:
                            f.write(new_encrypted_pwds)
                    self.communication_message('Master-key is successfully changed.')
        else:
            self.communication_message(f'{key} is incorrect key.')


app = App()
app.mainloop()

# todo:
# make better code
