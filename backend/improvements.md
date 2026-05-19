DURING SIGNUP PROCESS
Instead of manual duplicate check:

if user:

you can also rely on DB unique constraints and catch IntegrityError.

Because two signup requests can pass your check simultaneously (race condition).

Production apps usually do both:

validate early for better UX
still rely on DB unique constraints for actual safety
