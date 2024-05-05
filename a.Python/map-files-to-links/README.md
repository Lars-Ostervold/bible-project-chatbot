The files in this folder are designed to created json files that will be in the format of 

'file name': 'link','title', 'file name': 'link','title',....

It creates a map so that I can use the metadata return from Pinecone (which is the file name), then get the original source. This lets me suggest further material for the user.

For the 'script_refs', these are transcripts from videos. They don't really have direct links themselves and I couldn't figure out a good way to map the YouTube links to the scripts. So here I just return to the user for further material '{Title} video on either the BibleProject website or YouTube', which is sufficient for now. 

For 'study_notes', these are additional notes for theme videos. So I just linked to the study notes homepage and gave the title. The mapping is complicated because the site redirects you when you try to open the PDF of the study notes.