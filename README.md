# Mark notifier

Mark notifier is a simple tool which notifies a student by email when a new grade is added or changed in a course grade book. This tool works only for grade books organized in Google Sheet.

If there could not be found a perfect match by name in the grade book, the application will send notifications for the student with the closest name match (shortest Levenshtein distance).

It can be configured very easily with CRON job scheduler to run the tool every once in a while.
