def save_blog_to_file(blog_content, blog_title, 
        blog_meta_desc, blog_tags, blog_categories, main_img_path, file_type="md"):
    """ Common function to save the generated blog to a file.
    arg: file_type can be md or html
    """
    # Convert the spaces in blog_title with dash
    logger.info(f"The blog will be saved at: {output_path}")
    logger.debug(f"Blog Title is: {blog_title}")
    blog_title_md = blog_title
    regex = re.compile('[^a-zA-Z0-9- ]')
    blog_title_md = regex.sub('', blog_title_md)
    blog_title= blog_title.replace(":", "")
    blog_title_md = re.sub('--+', '-', blog_title_md)
    blog_title_md = blog_title_md.replace(' ', '-')
    blog_title_md = remove_stop_words(blog_title_md)

    if ':' in blog_meta_desc:
        blog_meta_desc  = blog_meta_desc.split(':')[1].strip()

    if not os.path.exists(output_path):
        logger.error("Error: Blog output directory is set to {output_path}, which Does Not Exist.")

    # Different output formats are plaintext, html and markdown.
    if file_type in "md":
        logger.info(f"Writing/Saving the resultant blog content in Markdown format.")
        # fill the Front Matter as below at the top of the post: https://jekyllrb.com/docs/front-matter/
        # date: YYYY-MM-DD HH:MM:SS +/-TTTT
        from zoneinfo import ZoneInfo
        tz=ZoneInfo('Asia/Kolkata')
        dtobj = datetime.datetime.now(tz=ZoneInfo('Asia/Kolkata'))
        formatted_date = f"{dtobj.strftime('%Y-%m-%d %H:%M:%S %z')}"

        blog_frontmatter = f"""\
                        ---
                        title: {blog_title}
                        date: {formatted_date}
                        categories: [{blog_categories}]
                        tags: [{blog_tags}]
                        description: {blog_meta_desc}
                        img_path: '/assets/'
                        image:
                            path: {os.path.basename(main_img_path)}
                            alt: {blog_title}
                        ---\n\n"""

        # Create a new file named YYYY-MM-DD-TITLE.EXTENSION and put it in the _posts of the root directory. 
        # Please note that the EXTENSION must be one of md or markdown
        blog_output_path = os.path.join(
                output_path,
                f"{datetime.date.today().strftime('%Y-%m-%d')}-{blog_title_md}.md"
                )
        # Save the generated blog content to a file.
        try:
            with open(blog_output_path, "w") as f:
                f.write(dedent(blog_frontmatter))
                f.write(blog_content)
        except Exception as e:
            raise Exception(f"Failed to write blog content: {e}")
        logger.info(f"\nSuccessfully saved and Posted blog at: {blog_output_path,}\n")


# Helper function
def remove_stop_words(sentence):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(sentence)

    # Get the list of English stop words
    stop_words = set(stopwords.words('english'))

    # Remove stop words from the sentence
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Join the filtered words back into a sentence
    filtered_sentence = ' '.join(filtered_words)

    return filtered_sentence
