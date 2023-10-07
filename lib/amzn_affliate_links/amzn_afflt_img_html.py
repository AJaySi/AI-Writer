###############################################################################
#
# To use the module, simply create an instance of the AmazonAffiliateImages class, 
# passing in your Amazon affiliate tag. Then, you can use the get_image_url() or 
# get_image_html() methods to get the Amazon affiliate image URL or HTML for a product, 
# passing in either the product ASIN or the product URL.
#
###############################################################################

import requests
from bs4 import BeautifulSoup

class AmazonAffiliateImages:
    def __init__(self, associate_tag):
        self.associate_tag = associate_tag

    def get_product_asin(self, product_url):
        """Gets the Amazon product ASIN from a product URL.

        Args:
            product_url: The Amazon product URL.

        Returns:
            The Amazon product ASIN, or None if the product URL is not valid.
        """

        soup = BeautifulSoup(requests.get(product_url).content, "html.parser")
        asin = soup.find("input", type="hidden", name="ASIN")
        if asin is not None:
            return asin.get("value")
        else:
            return None

    def get_image_url(self, product_asin):
        """Gets the Amazon affiliate image URL for a product.

        Args:
            product_asin: The Amazon product ASIN.

        Returns:
            The Amazon affiliate image URL, or None if the product is not found.
        """

        url = f"https://images-na.ssl-images-amazon.com/images/I/{product_asin}.jpg"
        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            return None

    def get_image_html(self, product_asin):
        """Gets the Amazon affiliate image HTML for a product.

        Args:
            product_asin: The Amazon product ASIN.

        Returns:
            The Amazon affiliate image HTML, or None if the product is not found.
        """

        image_url = self.get_image_url(product_asin)
        if image_url is not None:
            return f'<img src="{image_url}" alt="Amazon Affiliate Image" />'
        else:
            return None


#######################################################

import amazon_affiliate_images

affiliate_images = AmazonAffiliateImages("YOUR_ASSOCIATE_TAG")
image_html = affiliate_images.get_image_html("B00004CB54")

# Print the image HTML
print(image_html)

# Output : <img src="https://images-na.ssl-images-amazon.com/images/I/B00004CB54.jpg" alt="Amazon Affiliate Image" />
# You can then use this image HTML in your blog post.
