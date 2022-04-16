from converter import Converter

dir_path = "/Users/rnazmutdinov/Meetme/MeetMe-backend/src"

converter = Converter(dir_path)
converter.crete_class_table()
converter.crete_interface_table()
converter.crete_class_members_tables()
converter.crete_interface_members_tables()
converter.save_table("doc.docx")
