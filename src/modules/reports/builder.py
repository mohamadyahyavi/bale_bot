from src.modules.reports.schema import ReportSchema, ProjectReport


class ReportBuilder:


    def build_daily(self, user, logs, worked, missing, overtime, open_timer):

        projects = {}

        for item in logs:

            name = item["project"]
            duration = item["duration"] / 3600

            projects[name] = projects.get(name, 0) + duration


        project_list = [
            ProjectReport(project=k, hours=v)
            for k, v in projects.items()
        ]


        return ReportSchema(

            user_id=str(user.id),

            report_date=None,

            worked_hours=worked,
            required_hours=8,

            missing_hours=missing,
            overtime_hours=overtime,

            has_open_timer=open_timer,

            projects=project_list
        )