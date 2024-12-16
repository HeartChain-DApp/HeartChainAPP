        label = tk.Label(self.content_frame, text="Welcome to the Home page!", font=("Arial", 24))
        label.pack(pady=20)

        # Open and resize the images using Pillow
        img1 = Image.open("/Users/mac/Desktop/MST AISD/S3/Blockchain/Pr Ikram Ben abdelouahab/HeartChainAPP/a1.png")
        img2 = Image.open("/Users/mac/Desktop/MST AISD/S3/Blockchain/Pr Ikram Ben abdelouahab/HeartChainAPP/a2.png")

        # Resize the images to a smaller size (for example, 200x200 pixels)
        img1_resized = img1.resize((200, 200))  # Resize to 200x200
        img2_resized = img2.resize((200, 200))  # Resize to 200x200

        # Convert the resized images to Tkinter-compatible format
        img1_tk = ImageTk.PhotoImage(img1_resized)
        img2_tk = ImageTk.PhotoImage(img2_resized)

        # Create a frame to hold the images
        image_frame = tk.Frame(self.content_frame)
        image_frame.pack(pady=10)

        # Place the first image on the left
        img_label1 = tk.Label(image_frame, image=img1_tk)
        img_label1.image = img1_tk  # Keep reference to avoid garbage collection
        img_label1.pack(side="left", padx=10)

        # Place the second image on the right
        img_label2 = tk.Label(image_frame, image=img2_tk)
        img_label2.image = img2_tk  # Keep reference to avoid garbage collection
        img_label2.pack(side="right", padx=10)

        # Display the "Welcome back Doctor" message in the center
        welcome_label = tk.Label(self.content_frame, text="Welcome back Doctor", font=("Arial", 24), fg="green")
        welcome_label.pack(pady=20)