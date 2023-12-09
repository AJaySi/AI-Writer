

def generate_detailed_blog(num_blogs, blog_keywords, niche, num_subtopics,
        wordpress=False, research_online=False, output_format="HTML"):
    """
    This function will take a blog Topic to first generate sections for it
    and then generate content for each section.
    """
    # Use to store the blog in a string, to save in a *.md file.
    blog_markdown_str = ""

    # TBD: Check if the generated topics are equal to what user asked.
    blog_topic_arr = generate_blog_topics(blog_keywords, num_blogs, niche)
    logger.info(f"Generated Blog Topics:---- \n{blog_topic_arr}\n")
    # Split the string at newlines
    blog_topic_arr = blog_topic_arr.split('\n')

    # For each of blog topic, generate content.
    for a_blog_topic in blog_topic_arr:
        # if md/html
        a_blog_topic = a_blog_topic.replace('"', '')
        a_blog_topic = re.sub(r'^[\d.\s]+', '', a_blog_topic)
        blog_markdown_str = "# " + a_blog_topic + "\n\n"
        
        # Get the introduction specific to blog title and sub topics.
        tpc_outlines = generate_topic_outline(a_blog_topic, num_subtopics)
        tpc_outlines = tpc_outlines.split("\n")
        
        blog_intro = get_blog_intro(a_blog_topic, tpc_outlines)
        logger.info(f"The intro is:\n{blog_intro}")
        blog_markdown_str = blog_markdown_str + "### Introduction" + "\n\n" + f"{blog_intro}" + "\n\n"
        
        # Now, for each blog we have sub topic. Generate content for each of the sub topic.
        for a_outline in tpc_outlines:
            a_outline = a_outline.replace('"', '')
            logger.info(f"Generating content for sub-topic: {a_outline}")
            sub_topic_content = generate_topic_content(blog_keywords, a_outline)
            # a_outline is sub topic heading, hence part ToC also.
            #blog_markdown_str = blog_markdown_str + "\n\n" + f"### {a_outline}" + "\n\n"
            blog_markdown_str = blog_markdown_str + "\n" + f"\n {sub_topic_content}" + "\n\n"

        # Get the Conclusion of the blog, by passing the generated blog.
        blog_conclusion = get_blog_conclusion(blog_markdown_str)
        blog_markdown_str = blog_markdown_str + "### Conclusion" + "\n" + f"{blog_conclusion}" + "\n"

        # logger.info/check the final blog content.
        logger.info(f"Final blog content: {blog_markdown_str}")

        #if research_online:
        #    # Call on the got-researcher, tavily apis for this. So many apis floating around.
        #    report = do_online_research_on(blog_keywords)
        #    blog_markdown_str = blog_with_research(report, blog_markdown_str)

        blog_meta_desc = generate_blog_description(blog_markdown_str)
        logger.info(f"\nThe blog meta description is:{blog_meta_desc}\n")

        # Generate an image based on meta description
        logger.info(f"Calling Image generation with prompt: {blog_meta_desc}")
        main_img_path = generate_image(blog_meta_desc, image_dir, "dalle3")
        
        blog_tags = get_blog_tags(blog_markdown_str)
        logger.info(f"\nBlog tags for generated content: {blog_tags}\n")

        blog_categories = get_blog_categories(blog_markdown_str)
        logger.info(f"Generated blog categories: {blog_categories}\n")

        # Use chatgpt to convert the text into HTML or markdown.
        if 'html' in output_format:
            blog_markdown_str = convert_markdown_to_html(blog_markdown_str)

        # Check if blog needs to be posted on wordpress.
        if wordpress:
            # Fixme: Fetch all tags and categories to check, if present ones are present and
            # use them else create new ones. Its better to use chatgpt than string comparison.
            # Similar tags and categories will be missed.
            # blog_categories = 
            # blog_tags = 
            logger.info("Uploading the blog to wordpress.\n")
            main_img_path = compress_image(main_img_path, quality=85)
            try:
                img_details = analyze_and_extract_details_from_image(main_img_path)
                alt_text = img_details.get('alt_text')
                img_description = img_details.get('description')
                img_title = img_details.get('title')
                caption = img_details.get('caption')
                try:
                    media = upload_media(wordpress_url, wordpress_username, wordpress_password, 
                        main_img_path, alt_text, img_description, img_title, caption)
                except Exception as err:
                    sys.exit(f"Error occurred in upload_media: {err}")
            except Exception as e:
                sys.exit(f"Error occurred in analyze_and_extract_details_from_image: {e}")

            # Then create the post with the uploaded media as the featured image
            media_id = media['id']
            blog_markdown_str = convert_markdown_to_html(blog_markdown_str)
            try:
                upload_blog_post(wordpress_url, wordpress_username, wordpress_password, a_blog_topic, 
                        blog_markdown_str, media_id, blog_meta_desc, blog_categories, blog_tags, status='publish')
            except Exception as err:
                sys.exit(f"Failed to upload blog to wordpress.Error: {err}")

        # TBD: Save the blog content as a .md file. Markdown or HTML ?
        save_blog_to_file(blog_markdown_str,
                a_blog_topic,
                blog_meta_desc, blog_tags,
                blog_categories, main_img_path)

    # Now, we need perform some *basic checks on the blog content, such as:
    # is_content_ai_generated.py, plagiarism_checker_from_known_sources.py
    # seo_analyzer.py . These are present in the lib folder.
    # prompt: Rewrite, improve and paraphrase [text] and use headings and subheadings 
    # to break up the content and make it easier to read using the keyword [keyword].
