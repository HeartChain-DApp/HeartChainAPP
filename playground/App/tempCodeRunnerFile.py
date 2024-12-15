def show_audit(self):
        label = tk.Label(self.content_frame, text="Audit", font=("Arial", 24))
        label.pack(pady=20)
        columns = ("Timestamp", "Action", "User", "Record Hash", "Action Type")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        audit_logs = fetch_audit_logs() 
        if audit_logs:
            for audit in audit_logs:
                tree.insert("", "end", values=(audit["timestamp"], audit["action"], audit["user"], audit["record_hash"], audit["action_type"]))
        else:
            print("No audit logs available.")  

        tree.pack(pady=20, fill="both", expand=True)