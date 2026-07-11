from datetime import datetime, time,timedelta
from collections import defaultdict
from .client import KimaiClient
import httpx

class KimaiService:

    def __init__(self, client: KimaiClient):
        self.client = client

    def _today_range(self):

        now = datetime.now()

        begin = datetime.combine(
            now.date(),
            time.min,
        )

        return begin, now
    
    async def get_current_week_timesheets(
      self,
      kimai_user_id: int,
    ):

      now = datetime.now()

      days_since_saturday = (now.weekday() + 2) % 7
      week_start = now - timedelta(days=days_since_saturday)

      begin = datetime.combine(week_start.date(), time.min)
      end = now

      return await self.client.get(
        "/api/timesheets",
        params={
            "user": kimai_user_id,
            "begin": begin.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": now.strftime("%Y-%m-%dT%H:%M:%S"),
        },
      )
    

    async def create_timesheet(
       self,
       begin: str,
       end: str,
       project: int,
       activity: int,
       description: str,
       kimai_user_id: int,
       ):

        payload = {
        "begin": begin,
        "end": end,
        "project": project,
        "activity": activity,
        "description": description,
        "user": kimai_user_id,
        }


        try:
           return await self.client.post(
            "/api/timesheets",
            json=payload,
           )

        except httpx.HTTPStatusError as e:
          
          status_code = e.response.status_code
          response_body = e.response.text.lower()

          if status_code == 400:
              # خطای همپوشانی
              if (
                "overlap" in response_body
                or "overlapping" in response_body
                or "already" in response_body
                ):
                raise ValueError("OVERLAP")

              raise ValueError("INVALID_DATA")

          elif status_code == 401:
            raise ValueError("UNAUTHORIZED")

          elif status_code == 403:
            raise ValueError("FORBIDDEN")

          elif status_code == 404:
            raise ValueError("NOT_FOUND")

        # سایر خطاهای HTTP
          raise
        except httpx.RequestError:
          raise ValueError("CONNECTION_ERROR")

    
    

    async def get_current_month_timesheets(
      self,
      kimai_user_id: int,
      ):

      now = datetime.now()

      begin = datetime(
        year=now.year,
        month=now.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
      )

      return await self.client.get(
        "/api/timesheets",
        params={
            "user": kimai_user_id,
            "begin": begin.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": now.strftime("%Y-%m-%dT%H:%M:%S"),
        },
      )

    async def get_today_timesheets(
        self,
        kimai_user_id: int,
        ):

        begin, end = self._today_range()
        print ("THE FUNCTION GOT CALLED")

        return await self.client.get(
            "/api/timesheets",
            params={
                "user": kimai_user_id,
                "begin": begin.strftime("%Y-%m-%dT%H:%M:%S"),
                "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
            },
        )
    
    async def get_week_worked_duration(
      self,
      kimai_user_id: int,
      ) -> str:

      entries = await self.get_current_week_timesheets(
        kimai_user_id
      )

      total_seconds = sum(
        entry.get("duration", 0)
        for entry in entries
      )

      total_minutes = total_seconds // 60
   
      hours = total_minutes // 60
      minutes = total_minutes % 60

      return f"{hours}:{minutes:02d}"
    

    async def get_month_worked_duration(
      self,
      kimai_user_id: int,
    ) -> str:

      entries = await self.get_current_month_timesheets(
        kimai_user_id
      )

      total_seconds = sum(
        entry.get("duration", 0)
        for entry in entries
      )

      total_minutes = total_seconds // 60

      hours = total_minutes // 60
      minutes = total_minutes % 60

      return f"{hours}:{minutes:02d}"

    async def get_week_activity_duration(
       self,
       kimai_user_id: int,
    ):

       entries = await self.get_current_week_timesheets(
        kimai_user_id
       )

       activities = await self.get_all_activities()

       activity_names = {
        activity["id"]: activity["name"]
        for activity in activities
       }

       activity_seconds = defaultdict(int)

       for entry in entries:

          activity_id = entry.get("activity")

          if activity_id is None:
            continue

          activity_seconds[activity_id] += entry.get("duration", 0)

       result = []

       for activity_id, seconds in activity_seconds.items():
 
          total_minutes = seconds // 60
          hours = total_minutes // 60
          minutes = total_minutes % 60

          result.append({
            "activity": activity_names.get(
                activity_id,
                f"Activity {activity_id}"
            ),
            "duration": f"{hours}:{minutes:02d}"
          })

       return result
    
    async def get_month_activity_duration(self, kimai_user_id: int):

        entries = await self.get_current_month_timesheets(kimai_user_id)
        activities = await self.get_all_activities()

        activity_names = {
        activity["id"]: activity["name"]
        for activity in activities
        }

        activity_seconds = defaultdict(int)

        for entry in entries:
            activity_seconds[entry["activity"]] += entry.get("duration", 0)

        result = []

        for activity_id, seconds in activity_seconds.items():

            total_minutes = seconds // 60
            hours = total_minutes // 60
            minutes = total_minutes % 60

            result.append({
            "activity": activity_names.get(activity_id, str(activity_id)),
            "duration": f"{hours}:{minutes:02d}"
            })

        return result

    async def get_all_activities(self):

        return await self.client.get(
        "/api/activities"
        )

    async def get_all_projects(self):

        return await self.client.get(
        "/api/projects"
        )

    async def has_overlap(
    self,
    kimai_user_id: int,
    begin: datetime,
    end: datetime,
    ) -> bool:

      entries = await self.client.get(
        "/api/timesheets",
        params={
            "user": kimai_user_id,
            "begin": begin.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
        },
    )

      return len(entries) > 0    
    
    async def get_today_activity_durations(self, kimai_user_id: int):

        entries = await self.get_today_timesheets(kimai_user_id)
        activities = await self.get_all_activities()

        activity_names = {
        activity["id"]: activity["name"]
        for activity in activities
        }

        activity_seconds = defaultdict(int)

        for entry in entries:
            activity_seconds[entry["activity"]] += entry.get("duration", 0)

        result = []

        for activity_id, seconds in activity_seconds.items():

            total_minutes = seconds // 60
            hours = total_minutes // 60
            minutes = total_minutes % 60

            result.append({
            "activity": activity_names.get(
                activity_id,
                f"Activity {activity_id}"
            ),
            "duration": f"{hours}:{minutes:02d}"
            })

        return result

    async def get_month_delay_hours(self,kimai_user_id):

          entries = await self.get_current_month_timesheets(kimai_user_id)

          # گروه‌بندی بر اساس تاریخ
          daily_entries = defaultdict(list)

          for entry in entries:

            begin = datetime.fromisoformat(
            entry["begin"].replace("+0330", "+03:30")
            )

            daily_entries[begin.date()].append(begin)

          total_delay_seconds = 0

          for work_date, begins in daily_entries.items():

            first_begin = min(begins)

            official_start = datetime.combine(
            work_date,
            time(hour=9, minute=0),
            tzinfo=first_begin.tzinfo,
            )

            if first_begin > official_start:

               total_delay_seconds += (
                first_begin - official_start
               ).total_seconds()
          total_minutes = int(total_delay_seconds // 60)
          hours = total_minutes // 60
          minutes = total_minutes % 60     

          return f"{hours}:{minutes:02d}"  
    
    async def get_current_month_timesheets(
       self,
       kimai_user_id: int,
       ):
        now = datetime.now()

        begin = datetime(
        year=now.year,
        month=now.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
        )

        end = now


        return await self.client.get(
        "/api/timesheets",
        params={
            "user": kimai_user_id,
            "begin": begin.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
        },
    )    

    async def has_work_started_today(
        self,
        kimai_user_id: int,
    ) -> bool:

        entries = await self.get_today_timesheets(
            kimai_user_id
        )

        return bool(entries)

    def _month_range(self):
        now = datetime.now()

        begin = datetime(
        year=now.year,
        month=now.month,
        day=1
        )

        return begin, now    

    async def get_month_worked_duration(
        self,
        kimai_user_id: int,
    ) -> float:

        now = datetime.now()
        begin = datetime(
        year=now.year,
        month=now.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )


        entries = await self.client.get(
        "/api/timesheets",
        params={
            "user": kimai_user_id,
            "begin": begin.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": now.strftime("%Y-%m-%dT%H:%M:%S"),
        },
    )

        total_seconds = sum(entry.get("duration", 0) for entry in entries)

        return round(total_seconds / 3600, 2)
    

    async def get_today_worked_duration(
       self,
       kimai_user_id: int,
       ) -> str:

       entries = await self.get_today_timesheets(kimai_user_id)

       total_seconds = sum(
        entry.get("duration", 0)
        for entry in entries
       )

       total_minutes = total_seconds // 60

       hours = total_minutes // 60
       minutes = total_minutes % 60

       return f"{hours}:{minutes:02d}"
    
    async def get_today_overtime(
       self,
       kimai_user_id: int,
       ) -> str:

       entries = await self.get_today_timesheets(kimai_user_id)

       total_seconds = sum(
        entry.get("duration", 0)
        for entry in entries
       )

       overtime_seconds = max(0, total_seconds - (7 * 3600))

       total_minutes = overtime_seconds // 60

       hours = total_minutes // 60
       minutes = total_minutes % 60

       return f"{hours}:{minutes:02d}"
    

    async def has_active_timer(
        self,
        kimai_user_id: int,
    ) -> bool:

        timesheets = await self.get_today_timesheets(
        kimai_user_id
    )

        now = datetime.now().astimezone()

        return any(
        datetime.strptime(
            t["begin"],
            "%Y-%m-%dT%H:%M:%S%z"
        ) <= now <= datetime.strptime(
            t["end"],
            "%Y-%m-%dT%H:%M:%S%z"
        )
        for t in timesheets
        )

    async def get_active_timers(
        self,
        user_id: int,
    ):

        return await self.client.get(
            "/api/timesheets",
            params={
                "user": user_id,
                "active": 1,
            },
        )

    async def get_open_timesheets(
        self,
        kimai_user_id: int,
    ):

        entries = await self.client.get(
        "/api/timesheets",
        params={
            "user": kimai_user_id,
        },
    )


        return [
            entry
            for entry in entries
            if entry.get("end") is None
        ]

    async def get_today_report(
        self,
        user_id: int,
    ) -> dict:

        entries = await self.get_today_timesheets(
            user_id
        )

        worked_seconds = sum(
            entry.get("duration", 0)
            for entry in entries
        )

        active_timer = any(
            entry.get("end") is None
            for entry in entries
        )

        return {
            "has_entry": len(entries) > 0,
            "worked_seconds": worked_seconds,
            "worked_hours": worked_seconds / 3600,
            "active_timer": active_timer,
            "entries": entries,
        }