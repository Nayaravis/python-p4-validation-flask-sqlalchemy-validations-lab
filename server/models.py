from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validate_name(self, key, name):
        if name.strip() == "" or name is None:
            raise ValueError("name should not be empty")
        elif Author.query.filter_by(name=name).first():
            raise ValueError("username is already taken")
        return name

    @validates("phone_number")
    def validate_number(self, key, number):
        from string import digits
        if len(number) != 10:
            raise ValueError("phone_number must be 10 digits")
        
        for char in number:
            if char not in digits:
                raise ValueError("phone_number must be a digit")

        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    CATEGORIES = ["Fiction", "Non-Fiction"]
    CLICKBAIT_WORDS = ["Won't Believe", "Secret", "Top", "Guess"]
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title")
    def validate_title_exists(self, key, title):
        if title.strip() == '' or title == None:
            raise ValueError("title should not be empty")
        
        for clickbait_word in Post.CLICKBAIT_WORDS:
            if clickbait_word.lower() in title.lower():
                return title
        
        raise ValueError("title does not have any clickbait words")

    @validates("content")
    def validate_content_length(self, key, content):
        if len(content) < 250:
            raise ValueError("content must not be less than 250 characters")
        
        return content
    
    @validates("summary")
    def validate_summary_length(self, key, summary):
        if len(summary) > 250:
            raise ValueError("summary must not be more than 250 characters")
        
        return summary
    
    @validates("category")
    def validate_category(self, key, category):
        if category not in Post.CATEGORIES:
            raise ValueError(f"post category must be one of {Post.CATEGORIES}")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
