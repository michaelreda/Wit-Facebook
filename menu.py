from fbmq import Page,Template

PAGE_ACCESS_TOKEN = "EAAL0VIHjZAZAgBAIg0QRTxz3oEYXL6vr8crg5YCuIapca1AZAcghDCLg2QbX7epmw7WJtWSWqGZAk0KhdeTcHMBrM4cDZCZCLtzYIj04tZA4jp4XkCDWrxERZAZCmE1EZAjGOMF0ejS1zxaX4awgFZC4NZB5IaN0ZAfXTBIbF6MYQW9GWnQZDZD"

page = Page(PAGE_ACCESS_TOKEN)

page.show_persistent_menu([Template.ButtonPostBack('MENU1', 'MENU_PAYLOAD/1'),
						   Template.ButtonPostBack('MENU2', 'MENU_PAYLOAD/2')])

@page.callback(['MENU_PAYLOAD/(.+)'])
def click_persistent_menu(payload, event):
  click_menu = payload.split('/')[1]
  print("you clicked %s menu" % click_menu)
