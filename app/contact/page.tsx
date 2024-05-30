'use client';
import { useState } from 'react';


// To add: email logic, back to home button, and styling
//FIX: The children bit causes some issues when going back to the home page. 
//Need to figure out how the logic works. That's in layout.tsx. 

export default function ContactPage() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });

  const handleChange = (e: { target: { name: any; value: any; }; }) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();
  
    const response = await fetch('/api/sendEmail', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
  
    if (response.ok) {
      // Email sent successfully
      alert('Email sent successfully');
    } else {
      // Error sending email
      alert('Error sending email');
    }
  };

  //Class for input text box
  const inputClassName = "w-full mt-1 p-2 rounded-lg border border-gray-300 dark:border-black bg-sky-100 dark:bg-zinc-700";

return (
    <section className="flex items-center justify-center mt-[10vh]">
        <div className="card bg-white dark:bg-zinc-950 text-black dark:text-white rounded-lg shadow-md p-4 md:pd-2 border border-gray-400 dark:border-gray-600 overflow-hidden w-[40%]">
            <h1 className="font-medium text-3xl mb-2 tracking-tighter"> Contact us!</h1>
            <p className="prose prose-neutral dark:text-white mb-8">
                Questions, comments, or concerns? We'd love to hear from you! Just fill out the form below and we'll get back to you as soon as we can.
            </p>
            <form onSubmit={handleSubmit} className="space-y-4">
                <label className="block">
                    <span className="prose prose-neutral dark:text-white mb-8">Name:</span>
                    <input type="text" name="name" value={formData.name} onChange={handleChange} className={inputClassName} />
                </label>
                <label className="block">
                    <span className="prose prose-neutral dark:text-white mb-8">Email:</span>
                    <input type="email" name="email" value={formData.email} onChange={handleChange} className={inputClassName}/>
                </label>
                <label className="block">
                    <span className="prose prose-neutral dark:text-white mb-8">Message:</span>
                    <textarea name="message" value={formData.message} onChange={handleChange} className={inputClassName} />
                </label>
                <div className="flex justify-center">
                    <input type="submit" value="Submit" className="w-1/2 py-2 px-4 border dark:border-white rounded-lg bg-sky-200 dark:bg-slate-700 dark:text-white font-bold hover:bg-sky-500 dark:hover:bg-gray-800 transition-colors duration-200" />
                </div>
            </form>
        </div>
    </section>
);
}