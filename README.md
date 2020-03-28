NOTE:
Please install django crispy forms: pip install django-crispy-forms

ALL MINIMUM AND PREFERRED REQUIREMENTS HAVE BEEN SATISFIED

SPECS:
1. Registration system for IITD students (only using @iitd.ac.in - Email Verification by mailing not added).

2. There are two kinds of “entities” which are reviewed : Professors, and Courses.
Separate Pages have been made for each Professor and Course. Reviews can be viewed on the page of the particular professor or course. The reviews even have a detail view. They can be created, edited and deleted. Each user can only write one review per professor/course. THE AUTHOR CAN EDIT AND DELETE THEIR REVIEW FROM THE DETAIL VIEW WHICH CAN BE ACCESSED BY CLICKING THE TITLE OF THE REVIEW.

3. Guest Users have read only rights.

4. Registered users have a profile page where they can view their basic info and Respect Points and the posts they have created recently.

5. Registered Users can create professors, courses, their reviews and can like/dislike a review and even report a review.
These features are not available for guest users.

6. There is a search bar to search for professors and courses. It gives suggestions while the user types and then takes the input and lists all professors/courses matching the search query.

7. The admin -> /admin route has access to all the professors, courses, reports, users, profiles.

8. The admin can view all posts in the admin panel. The admin has options to see either the reported posts with the user who reported the post in P_Rev_Report/C_Rev_Report Models or order the posts according to the number of reports in the Prof_Review/Course_Review Models. Admin Actions have been created to allow either to delete all the reports of a post, or delete the post itself and warn the author of the post. Warning the author of the post will send them a message whenever they login the next time.

9. Admin Actions have also been created to BAN users in the User Model. There has two options: 
  i) a 15 day ban
  ii) a permanent ban
  Banning bans the email-id from re-registering during the duration.
  
10. The admin can also order the posts according to their date created. This allows a check on the recent activity of the users.

11. LIKE/DISLIKE: The reviews can be liked/disliked by registered users. The users have RESPECT POINTS which are 10 x the number of likes on their posts. This is to show the credibility of the users' reviews. A user cannot like their own posts.



SALIENT FEATURES:
1. Search Bar
2. Like/Dislike (AND RESPECT POINTS OF AUTHOR)
3. Report
4. Warnings & Ban (BONUS ASSIGNMENT)

Drawbacks:
1. No separate user logs stored(time deficit)



PART 1:
https://docs.google.com/document/d/1wZjWolhnYoU0lpHIJt-5kDbk4d6OWOfLwI4hrdtIGoA/edit?usp=sharing
