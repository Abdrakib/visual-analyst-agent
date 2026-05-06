import plotly.express as px


def draw_chart(visual_type: str, data: dict):
    try:
        if not data or "error" in data:
            return None

        labels = data.get("labels", [])
        values = data.get("values", [])
        series = data.get("series_name", "Value")

        if not labels or not values:
            return None

        vtype = visual_type.lower()

        if "bar" in vtype:
            fig = px.bar(
                x=labels, y=values,
                labels={"x": "Category", "y": series},
                title=series,
                color=values,
                color_continuous_scale=["#5a52e8", "#9333ea"]
            )
        elif "line" in vtype:
            fig = px.line(
                x=labels, y=values,
                labels={"x": "Category", "y": series},
                title=series,
                markers=True
            )
            fig.update_traces(
                line_color="#6c63ff",
                marker=dict(color="#a855f7", size=8)
            )
        elif "pie" in vtype or "donut" in vtype:
            fig = px.pie(
                names=labels, values=values,
                title=series,
                color_discrete_sequence=[
                    "#5a52e8", "#9333ea", "#38bdf8",
                    "#34d399", "#fbbf24", "#f87171"
                ]
            )
        elif "scatter" in vtype:
            fig = px.scatter(
                x=labels, y=values,
                labels={"x": "X", "y": series},
                title=series
            )
            fig.update_traces(marker=dict(color="#6c63ff", size=10))
        else:
            fig = px.bar(
                x=labels, y=values,
                labels={"x": "Category", "y": series},
                title=series,
                color=values,
                color_continuous_scale=["#5a52e8", "#9333ea"]
            )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(12,12,24,1)",
            font=dict(color="#8a88a0", family="system-ui"),
            title_font=dict(color="#c8c0f0", size=14),
            xaxis=dict(gridcolor="#1a1a2e", color="#4a4a6a"),
            yaxis=dict(gridcolor="#1a1a2e", color="#4a4a6a"),
            coloraxis_showscale=False,
            margin=dict(t=40, b=20, l=20, r=20)
        )
        return fig

    except Exception:
        return None
