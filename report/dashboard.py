from fasthtml.common import *
import matplotlib.pyplot as plt

from employee_events import Employee, Team
from utils import load_model

from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent


class ReportDropdown(Dropdown):
    """Dropdown component for selecting reports."""
    
    def build_component(self, entity_id, model):
        """Build dropdown using the model's name as label."""
        self.label = model.name
        return super().build_component(entity_id, model)
    
    def component_data(self, entity_id, model):
        """Return names and IDs for the dropdown options."""
        return model.names()


class Header(BaseComponent):
    """Header component displaying the model name."""

    def build_component(self, entity_id, model):
        """Build a header with the model's name."""
        return H1(model.name.capitalize() + ' Performance')


class LineChart(MatplotlibViz):
    """Line chart visualization for cumulative event counts."""
    
    def visualization(self, entity_id, model):
        
        x_y_data = model.event_counts(entity_id).fillna(0)
        x_y_data = x_y_data.set_index("event_date").sort_index().cumsum()
        x_y_data.columns = ['Positive', 'Negative']

        fig, ax = plt.subplots(figsize=(7, 6))
        x_y_data.plot(ax=ax, linewidth=2, linestyle='-')
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        ax.set_title("Cumulative Event Counts")
        ax.set_xlabel("Date")
        ax.set_ylabel("Event Count")
        ax.grid(True, linestyle='--', alpha=0.5)
        fig.autofmt_xdate()


class BarChart(MatplotlibViz):
    """Bar chart visualization for recruitment risk prediction."""

    predictor = load_model()

    def visualization(self, entity_id, model):
        """Visualize predicted recruitment risk as a bar chart."""
        data = model.model_data(entity_id)
        proba = self.predictor.predict_proba(data)
        prob_column = proba[:, 1]
        
        pred = prob_column.mean() if model.name == 'team' else prob_column[0]
        
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")


class Visualizations(CombinedComponent):
    """Component combining line chart and bar chart visualizations."""
    
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')


class NotesTable(DataTable):
    """DataTable component displaying user notes."""

    def component_data(self, entity_id, model):
        """Retrieve notes for the given entity ID."""
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    """Form group for dashboard filters."""
    
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]


class Report(CombinedComponent):
    """Main report component combining all dashboard parts."""
    
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


# Initialize app and report
app, route = fast_app()
report = Report()


# Define routes
@route('/')
def get():
    """Return default report for Employee with ID 1."""
    return report(1, Employee())

@route('/employee/{id}')
def get(id: str):
    """Return report page for an employee by ID."""
    return report(id, Employee())

@route('/team/{id}')
def get(id: str):
    """Return report page for a team by ID."""
    return report(id, Team())

# Update dropdown options based on profile type
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    profile_type = r.query_params['profile_type']
    if profile_type == 'Team':
        return dropdown(None, Team())
    elif profile_type == 'Employee':
        return dropdown(None, Employee())

# Handle form submission and redirect
@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

# Start the server
serve()
